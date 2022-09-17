function verifyid(){
    if((document.getElementById("id").value).match((/^([nN]{1})(18)([1234567890]{4})$/im))!=null){
        document.getElementById("id").style.borderColor="green";
        return true;
    }
    else{
        document.getElementById("id").style.borderColor="red";
        return false;
    }
}