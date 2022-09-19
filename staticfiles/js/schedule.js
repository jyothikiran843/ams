html_data="";
const days={'Monday':'m','Tuesday':'tu','Wednesday':'w','Thursday':'th','Friday':'f','Saturday':'s'};
const subjects={'Software Engineering':'se','Mathematical Fundamentals for DS':'mfds','Data Mining':'dm','Operating System':'os','Computer Networks':'cn','Computer Networking Lab':'cnl','Software Engineering Lab':'sel','English Lab':'el','Operating Systems Lab':'osl'}
form=Array.from(document.getElementsByTagName('form')[0]);
console.log(form)
for(var day in days){
    var div=document.createElement('div');
    div.setAttribute('class','form-row');

    for(var subject in subjects){
        
    }
}