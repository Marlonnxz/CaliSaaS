<#import "template.ftl" as layout>
<@layout.registrationLayout displayMessage=false; section>

<#if section = "form">
<div class="custom-login">

    <h1>CaliSaaS</h1>
    <p>Acceso seguro</p>

    <form id="kc-form-login" action="${url.loginAction}" method="post">
        
        <input type="text" name="username" placeholder="Usuario" required />
        
        <input type="password" name="password" placeholder="Contraseña" required />
        
        <button type="submit">Entrar</button>
    </form>

</div>
</#if>

</@layout.registrationLayout>