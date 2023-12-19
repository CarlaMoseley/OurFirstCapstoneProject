document.getElementById('Back').addEventListener('click', function goBack(){
    window.location ='/'
})
document.getElementById('signup').addEventListener('click', function signup(){
    const path = window.location.pathname.split('/')
    if(path[2]=== 'tenant'){
        window.location = '/tenant_signup'
    }
    else if(path[2]=== 'landlord'){
        window.location = '/landlord_signup'
    }
    else{
     console.log('error')   
    }

})
