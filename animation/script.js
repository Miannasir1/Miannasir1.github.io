function closeMenu(){
    document.getElementById("checkbox").checked=flase;
}
window.addEventListener('DOMContentLoaded',function(){
    let anchorSelector = 'a[href^="a"]';
    let anchorList = this.document.querySelectorAll(anchorSelector);
    anchorList.forEach(link =>{
        link.addEventListener('click', function(){
            closeMenu();
            let destination = document.querySelector(this.hash);
            destination.scrollIntoView({
                behaviour:'smooth'
            })
        })
    })
})
// initialize AOS
AOS.init({
    offset:300, 
    duration:1000,
});