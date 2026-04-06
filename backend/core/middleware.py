import threading

_thread_locals = threading.local()

def get_current_user():
    return getattr(_thread_locals, 'user', None)

class TenantMiddleware:
    """
    Middleware que guarda el usuario autenticado en la variable global por hilo,
    permitiendo que los Modelos/Managers sepan quién está ejecutando la petición 
    sin necesidad de pasar el request explícitamente y así filtrar los queries (Multi-tenancy).
    
    Nota: Django REST Framework procesa la autenticación después de los middlewares base.
    Pero como usamos JWTAuthentication, DRF inyecta el request.user en la vista. 
    Para interceptarlo globalmente antes de las views o en las views, a veces se hace
    un middleware especial o se establece en un `APIView`. 
    Como el modelo no tiene request, guardaremos el request acá y si el user
    es AnonymousUser (porque DRF no ha corrido), lo actualizaremos en las vistas.
    Sin embargo, DRF Authentication corre en las vistas. Así que el middleware
    debe inyectar un hook o podemos usar una utilidad.
    Para que funcione con DRF JWT de caja, lo mejor es guardar el `request` y evaluar `request.user` de forma perezosa.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.request = request
        response = self.get_response(request)
        if hasattr(_thread_locals, 'request'):
            del _thread_locals.request
        return response

def get_current_request():
    return getattr(_thread_locals, 'request', None)
