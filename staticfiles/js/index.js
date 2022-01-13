console.log("hello world");

gsap.registerPlugin("ScrollTrigger");
gsap.from(".prop-col",{
scrollTrigger:{
    trigger:".prop-col",
    
    // markers:true,
    start: "center 80% "
},
  y:"-180",
duration:"0.6",
ease:"power2.in",
stagger:"0.2",
opacity:"0",
});

gsap.from("#head",{
    scrollTrigger:{
        trigger:"#head",
        // markers:true,
        start:"70% center"

    },
   y:"-150",
   opacity:"0",
    duration:"1.2",
    ease:"power2.inOut",
    color:"purple"
});

gsap.from("#first-text",{
    scrollTrigger:{
        trigger:"#first-text",
        // markers:true,
        start:"35% center"
    },
    color:"#892bdb",
    duration:"1",
    ease:"powerOut"
});

gsap.from("#last-para",{
    scrollTrigger:{
        trigger:"#last-para",
        // markers:true,
        start:"center center"

    },
    opacity:"0",
    x:"-50%",
    duration:"1",
    ease:"power2.in"

})

gsap.to(".head1",{
    scrollTrigger:{
        trigger:".head1",
        // markers:true
    },
    
    ease:"powerinOut",
    duration:"1.5",
})

var img=document.getElementById("java");
var div=document.getElementById("main-box");
var text=document.querySelector("#first-text");
var photo=document.querySelector("#photo");

// photo.innerHTML="2392904.jpg";


var arr=["#4545d4","#60c14d","#b85316","#892bdb"];
var arr2=["#9f6c0e","white","black","#381aaa"];
// var arr3=["img\2392904.jpg"]
var int=0;

// text.style.color="red";
img.addEventListener("click",changeColour=()=>{
    div.style.backgroundColor=arr[int];
    
    text.style.color=arr2[int];
    int++;
    if(int>=arr.length){
    int=0;
    }

    });

// var arr=["red","blue","green","orange"];
// var int=0;
// var changeColour=()=>{
// div.style.backgroundColor=arr[int];
// int++;
// console.log("i am running");
// }

var btn=document.querySelector("#scroll_top");

const toTop=()=>
{
    window.scrollTo({top:0,behavior:"smooth"});
}

btn.addEventListener("click",toTop);

var whole=0;
var single=0;



const typeWriter=()=>
{
    var text="";
    var letter="";
    var arr=["Plagiarism Finder ","Making Future Possible","Using Advance Algorithms","Machine learning Technology","Searching thousands of webpages"];
    
   

    text=arr[whole];
    letter=text.slice(0,single++);
    // if(int<=text.length) single++;
if(text.length==letter.length)
{
    whole++;
    single=0;
}

if(whole==arr.length)whole=0;
    document.querySelector("#plagiarism").textContent=letter;
      
// console.log(whole);


}

setInterval(typeWriter,200);
