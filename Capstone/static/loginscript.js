document.getElementById('Back').addEventListener('click', function goBack(){
    window.location ='/';
});
document.getElementById('signup').addEventListener('click', function signup(){
    const path = window.location.pathname.split('/')
    if(path[1]=== 'tenant'){
        window.location = '/tenant/signup'
    }
    else if(path[1]=== 'landlord'){
        window.location = '/landlord/signup'
    }
    else{
     console.log('error')   
    }

})
