document.getElementById('menu').addEventListener('click', function goBack(){
    window.location ='/';
})
document.getElementById('login').addEventListener('click', function returnToLogin(e){
        const path = window.location.pathname;
        if(path.includes('landlord')){
            window.location = '/login/landlord';
        }else if(path.includes('tenant')){
            window.location='/login/tenant';
        }else{
            console.error('Wrong URL PATH or value entered');
        }
})
