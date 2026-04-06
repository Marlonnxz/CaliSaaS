const Dashboard = () => {
  return (
    <div className="bg-blue-900/20 border border-blue-500/30 rounded-xl p-6 shadow-lg">
      <div className="flex items-center mb-4">
        <span className="text-2xl mr-3">👑</span>
        <h3 className="text-xl font-bold text-blue-400">Zona de Administración</h3>
      </div>
      <p className="text-gray-300 mb-4">
        Como dueño de gimnasio, aquí podrás ver los pagos, métricas y gestionar a tus atletas. 
      </p>
      <div className="grid grid-cols-2 gap-4">
        <button className="bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-lg font-medium">
          Gestionar Pagos
        </button>
        <button className="bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-lg font-medium">
          Ver Atletas
        </button>
      </div>
    </div>
  );
};

export default Dashboard;
