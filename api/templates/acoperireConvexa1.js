window.onload = main;
var minx = 0, miny = 0;
function main() {
    var i, n = 3;
	//canvas
	c = document.getElementById("myCanvas");
	ctx = c.getContext("2d");

	var input = document.getElementById("input");
	//input.addEventListener("mouseout",function(){ input.innerHTML="Introduceti centrele cercurilor (x,y)"});
	input.onclick = function(){ input.innerHTML="";}
	
    var load = document.getElementById("read");
	
	var aux= document.getElementById("inputA");
	aux.onclick = function(){aux.value="";}
	
	load.onclick = loadInput;
	
	mx = 0;
	
	graham = document.getElementById("graham");
	graham.style.visibility = "hidden";
	
	graham.addEventListener("click",drawGraham,false);
	
	run = document.getElementById("run");
	run.style.visibility = "hidden";
	
	run.onclick = calcA;
    
}

function distanta(a, b){
	//return Math.sqrt(Math.pow((Number(b.y) - Number(a.y), 2) + Math.pow(Number(b.x) - Number(a.x), 2)));
	var s1,s2,sqrt;
	s1=(b.y-a.y)*(b.y-a.y);
	s2=(b.x -a.x)*(b.x-a.x);
	sqrt=Math.sqrt(s1+s2);
	return sqrt;
}
function clearScreen(){
	ctx.clearRect(0, 0, c.width, c.height);
	ctx.lineWidth = 1;
	ctx.strokeStyle = "black";	
}

function drawGraham(){
	ctx.beginPath();
	ctx.strokeStyle="#FF0000";
	ctx.lineWidth=2;
	run.style.visibility="visible";
	ctx.moveTo(copy[l[0].poz].x/mx *250 + 300, 600 - (copy[l[0].poz].y/mx *250 + 300));
	
	for(i= 1; i< l.length; i++){
		var x = copy[l[i].poz].x/mx *250 + 300;
		var y = copy[l[i].poz].y/mx *250 + 300;
		
		
		ctx.lineTo(x,600-y);
	} 
	ctx.lineTo(copy[l[0].poz].x/mx *250 + 300,600 - (copy[l[0].poz].y/mx *250 + 300));
	ctx.stroke();
	findAndDrawCorners();
	
	
}

function findAndDrawCorners(){
	var i;
	for(i=0;i<l.length-1;i++){
		var slope; //panta
				
		if(copy[l[i+1].poz].y - copy[l[i].poz].y == 0)
			slope = 0;
		else
			slope = -(copy[l[i+1].poz].x - copy[l[i].poz].x)/(copy[l[i+1].poz].y - copy[l[i].poz].y);
				
				
		var t = 1/Math.sqrt(1+slope*slope);
				
		var b,c,d,e;
		if(copy[l[i+1].poz].y - copy[l[i].poz].y == 0) {
			b = {x: copy[l[i].poz].x, y: copy[l[i].poz].y + 1};
			c = {x: copy[l[i+1].poz].x, y: copy[l[i+1].poz].y + 1};
			d = {x: copy[l[i+1].poz].x, y: copy[l[i+1].poz].y - 1};
			e = {x: copy[l[i].poz].x, y: copy[l[i].poz].y - 1};
					
		}
		else {
			b = {x: copy[l[i].poz].x + t, y: copy[l[i].poz].y + slope*t};
			c = {x: copy[l[i+1].poz].x + t, y: copy[l[i+1].poz].y + slope*t};
			d = {x: copy[l[i+1].poz].x - t, y: copy[l[i+1].poz].y - slope*t};
			e = {x: copy[l[i].poz].x - t, y: copy[l[i].poz].y - slope*t};
		}
		ctx.strokeStyle="#FF0000";
		ctx.lineWidth=0.5;
		ctx.beginPath();
		ctx.moveTo(b.x/mx *250 + 300,600 - (b.y/mx *250 + 300));
		ctx.lineTo(c.x/mx *250 + 300,600 - (c.y/mx *250 + 300));
		ctx.lineTo(d.x/mx *250 + 300,600 - (d.y/mx *250 + 300));
		ctx.lineTo(e.x/mx *250 + 300,600 - (e.y/mx *250 + 300));
		ctx.lineTo(b.x/mx *250 + 300,600 - (b.y/mx *250 + 300));
				
		ctx.stroke();
	}
	var slope;
	if(copy[l[l.length-1].poz].y - copy[l[0].poz].y == 0)
		slope = 0;
	else
		slope = -(copy[l[l.length-1].poz].x - copy[l[0].poz].x)/(copy[l[l.length-1].poz].y - copy[l[0].poz].y);
	
	var t = 1/Math.sqrt(1+slope*slope);
			
	var b,c,d,e;
			
	if(copy[l[l.length-1].poz].y - copy[l[0].poz].y == 0) {
		b = {x: copy[l[l.length-1].poz].x, y: copy[l[l.length-1].poz].y + 1};
		c = {x: copy[l[0].poz].x, y: copy[l[0].poz].y + 1};
		d = {x: copy[l[0].poz].x, y: copy[l[0].poz].y - 1};
		e = {x: copy[l[l.length-1].poz].x, y: copy[l[l.length-1].poz].y - 1};
	}
	else {
		b = {x: copy[l[l.length-1].poz].x + t, y: copy[l[l.length-1].poz].y + slope*t};
		c = {x: copy[l[0].poz].x + t, y: copy[l[0].poz].y + slope*t};
		d = {x: copy[l[0].poz].x - t, y: copy[l[0].poz].y - slope*t};
		e = {x: copy[l[l.length-1].poz].x - t, y: copy[l[l.length-1].poz].y - slope*t};
	}
	
	ctx.moveTo(b.x/mx *250 + 300,600 - (b.y/mx *250 + 300));
	ctx.lineTo(c.x/mx *250 + 300,600 - (c.y/mx *250 + 300));
	ctx.lineTo(d.x/mx *250 + 300,600 - (d.y/mx *250 + 300));
	ctx.lineTo(e.x/mx *250 + 300,600 - (e.y/mx *250 + 300));
	ctx.lineTo(b.x/mx *250 + 300,600 - (b.y/mx *250 + 300));
	ctx.stroke();
}


function calcA(){
	var input = document.getElementById("inputA");
	var coord = input.value.split(" ");
	
	a = {x: coord[0], y: coord[1]};
	mx = Math.max(Math.abs(a.x),Math.abs(a.y));
		
		
	loadInput();
	drawGraham();
	
	
	if(isNaN(a.x) || isNaN(a.y)){
		alert("Punctul inserat nu este valid!");
	}
	else{
			
		ctx.beginPath();
		ctx.strokeStyle = "green";
		ctx.fillStyle = "green";
		ctx.arc(a.x/mx *250 + 300,600-(a.y/mx *250 + 300),3,0,2*Math.PI);
		ctx.stroke();
		ctx.fill();

		
		var v = [];
		var i;
		for(i=0;i<l.length;i++){
			v.push({x: copy[l[i].poz].x , y: copy[l[i].poz].y});
		}
		
		var n = l.length;
		
		var ok=1;
		if(l.length>2)
		{
			for(i=0;i<l.length-1;i++) {
				if(viraj(copy[l[i].poz],copy[l[i+1].poz],a)<0) {
					ok=0;
					break;
				}
			}
			if(viraj(copy[l[l.length-1].poz],copy[l[0].poz],a)<0)
				ok=0;
		}
		else
			if(l.length==2)
			{
				var d1= distanta(l[0],l[1]);
				var d2= distanta(l[0],a);
				var d3= distanta(l[1],a);
				if(d1 != d2+d3)
					ok=0;
			}
			else
				ok=0;
		
		
		if(ok==0) {
			//verifica in interiorul cercurilor
			for(i=0;i<v.length;i++){
				if(distanta(v[i], a) <=1){
					ok=1;
					break;
				}
			}
			
		//verifica in interiorul dreptunghiurilor
			for(i=0;i<l.length-1;i++) {
				var slope; //panta
				
				if(copy[l[i+1].poz].y - copy[l[i].poz].y == 0)
					slope = 0;
				else
					slope = -(copy[l[i+1].poz].x - copy[l[i].poz].x)/(copy[l[i+1].poz].y - copy[l[i].poz].y);
				
				
				var t = 1/Math.sqrt(1+slope*slope);
				
				var b,c,d,e;
				if(copy[l[i+1].poz].y - copy[l[i].poz].y == 0) {
					b = {x: copy[l[i].poz].x, y: copy[l[i].poz].y + 1};
					c = {x: copy[l[i+1].poz].x, y: copy[l[i+1].poz].y + 1};
					d = {x: copy[l[i+1].poz].x, y: copy[l[i+1].poz].y - 1};
					e = {x: copy[l[i].poz].x, y: copy[l[i].poz].y - 1};
					
				}
				else {
					b = {x: copy[l[i].poz].x + t, y: copy[l[i].poz].y + slope*t};
					c = {x: copy[l[i+1].poz].x + t, y: copy[l[i+1].poz].y + slope*t};
					d = {x: copy[l[i+1].poz].x - t, y: copy[l[i+1].poz].y - slope*t};
					e = {x: copy[l[i].poz].x - t, y: copy[l[i].poz].y - slope*t};
				}
				
				var pct = [];
				pct.push(b);
				pct.push(c);
				pct.push(d);
				pct.push(e);
				
				
				var m = {x: a.x, y: a.y};
				var result = inDreptunghi(pct,m);
				
				
				
				if(result == 1) {
					ok = 1;
					break;
				}
			}
			
			if(ok == 0) {
				var slope;
				if(copy[l[l.length-1].poz].y - copy[l[0].poz].y == 0)
					slope = 0;
				else
					slope = -(copy[l[l.length-1].poz].x - copy[l[0].poz].x)/(copy[l[l.length-1].poz].y - copy[l[0].poz].y);
				
				var t = 1/Math.sqrt(1+slope*slope);
				
				var b,c,d,e;
				
				if(copy[l[l.length-1].poz].y - copy[l[0].poz].y == 0) {
					b = {x: copy[l[0].poz].x, y: copy[l[0].poz].y + 1};
					c = {x: copy[l[l.length-1].poz].x, y: copy[l[l.length-1].poz].y + 1};
					d = {x: copy[l[0].poz].x, y: copy[l[0].poz].y - 1};
					e = {x: copy[l[l.length-1].poz].x, y: copy[l[l.length-1].poz].y - 1};
				}
				else {
					b = {x: copy[l[0].poz].x + t, y: copy[l[0].poz].y + slope*t};
					c = {x: copy[l[l.length-1].poz].x + t, y: copy[l[l.length-1].poz].y + slope*t};
					d = {x: copy[l[0].poz].x - t, y: copy[l[0].poz].y - slope*t};
					e = {x: copy[l[l.length-1].poz].x - t, y: copy[l[l.length-1].poz].y - slope*t};
				}
				
				var pct = [];
				pct.push(b);
				pct.push(c);
				pct.push(d);
				pct.push(e);
				
				
				var m = {x: a.x, y: a.y};
				var result = inDreptunghi(pct,m);
				if(result == 1)
					ok = 1;
			}
			if(ok == 0)
				alert("Punctul A nu apartine acoperirii convexe");
			else
				alert("Punctul A apartine acoperirii convexe");
			
		}
		else
			alert("Punctul A apartine acopeririri convexe");
	}
}
function inDreptunghi(a,m) {
	var i;
	
	for(i=0;i<4;i++)
    {
        var a1,a2,a3,A; //SUNT ARII BAI!!
        A=a[i].x*a[(i+1)%4].y + a[(i+1)%4].x*a[(i+2)%4].y + a[(i+2)%4].x*a[i].y - a[(i+2)%4].x*a[(i+1)%4].y - a[i].x*a[(i+2)%4].y - a[(i+1)%4].x*a[i].y;
        A=Math.abs(A);
        A*=0.5;

        a1=a[i].x*a[(i+1)%4].y + a[(i+1)%4].x*m.y + m.x*a[i].y - m.x*a[(i+1)%4].y - a[i].x*m.y - a[(i+1)%4].x*a[i].y;
        a2=m.x*a[(i+1)%4].y + a[(i+1)%4].x*a[(i+2)%4].y + a[(i+2)%4].x*m.y - a[(i+2)%4].x*a[(i+1)%4].y - m.x*a[(i+2)%4].y - a[(i+1)%4].x*m.y;
        a3=a[i].x*m.y + m.x*a[(i+2)%4].y + a[(i+2)%4].x*a[i].y - a[(i+2)%4].x*m.y - a[i].x*a[(i+2)%4].y - m.x*a[i].y;

        a1=Math.abs(a1); a1*=0.5;
        a2=Math.abs(a2); a2*=0.5;
        a3=Math.abs(a3); a3*=0.5;
		
		var res = a1+a2+a3;
		res = Math.round(res * 100)/100;
		A = Math.round(A * 100)/100;
		
        if(A==res)
        {
            return 1;
            break;
        }
    }
	
	if(i==4)
		return 0;
	
}
function loadInput() {
	 

	run.style.visibility = "hidden";
	clearScreen();
	//reinitialize all variables :)
    var v = [];
    
	graham.style.visibility = "visible";
    v.toString = function () { //Override toString for an Array of Objects
        var temp = "";
        for (i = 0; i < v.length; i++) {
            temp = temp + v[i].x + " " + v[i].y + "\n";
        }
        return temp;
    };

    var i;
    
	minx=0;
	miny=0;

    var input = document.getElementById("input");
    var splitLines = input.value.split("\n");
    for (i = 0; i < splitLines.length; i++) {
        var pair = splitLines[i].split(" ");
        v.push({x: Number(pair[0]), y: Number(pair[1]), poz: i}); //explicit conversion
        if (Number(pair[0]) < minx)
            minx = Number(pair[0]);
        if (Number(pair[1]) < 0)
            miny = Number(pair[1]);
    }
   
    //sa facem si o copie totusi ca sa afisam valorile initiale nu numai pozitia
    copy = [];
    for (i = 0; i < v.length; i++) {
        copy.push({x: v[i].x, y: v[i].y, poz: v[i].poz});
    }

    // ar trebui sa fie 1/n * v[0] + 1/n * v[1] + ... + 1/n * v[n-1]
    var bar = {x: 0, y: 0};

    var n = v.length; //ca sa nu mai scriu de fiecare data
    for (i = 0; i < v.length; i++) {
        bar.x = bar.x + (1 / n) * v[i].x;
        bar.y = bar.y + (1 / n) * v[i].y;
    }

	//Ar trebui sa ne ajute la desenarea punctelor
     //mx = 0;
    for (i = 0; i < copy.length; i++) {
        if (Math.abs(copy[i].x)+1 > mx)
            mx = Math.abs(copy[i].x)+1;
        if (Math.abs(copy[i].y)+1 > mx)
            mx = Math.abs(copy[i].y)+1;
    }
	
	
   
	
	//draw
	ctx.beginPath();
	ctx.moveTo(300,0);
	ctx.lineTo(300,600);
	ctx.stroke();
	
	ctx.moveTo(0,300);
	ctx.lineTo(600,300);
	ctx.stroke();
	
	for(i=-300;i<=c.width/2;i++){
		ctx.moveTo(i/mx*250+300,300-1/mx*25);
		ctx.lineTo(i/mx*250+300,300+1/mx*25);
		ctx.stroke();
	}
	for(i=-300;i<=c.height/2;i++){
		ctx.moveTo(300-1/mx*25,600 - (i/mx *250 + 300));
		ctx.lineTo(300+1/mx*25,600 - (i/mx *250 + 300));
		ctx.stroke();
	}
    for(i= 0; i< v.length; i++){
		var x = v[i].x/mx *250 + 300;
		var y = v[i].y/mx *250 + 300;
		
		ctx.beginPath();
		ctx.arc(x,600-y,1/mx*250,0,2*Math.PI);
		ctx.stroke();
	} 
	
    //translatia punctelor dupa baricentrul bar
    for (i = 0; i < v.length; i++) {
        v[i].x -= bar.x;
        v[i].y -= bar.y;
    }
    
    bar.x = 0;
    bar.y = 0;
	if(v.length>2){
		sort(v, bar);
		l = grahams_scan(v);
	}
	else
		l=v;
			
    
}
//q1-p1   r1-p1
//q2-p2   r2-p2
// (q1-p1)(r2-p2) - (q2-p2)(r1-p1);
function grahams_scan(v) {
    var list = [];
    list.push(v[0]);
    list.push(v[1]);
    for (var i = 2; i < v.length; i++) {
        list.push(v[i]);
        while (list.length > 2 && viraj(list[list.length - 3], list[list.length - 2], list[list.length - 1]) <= 0)
            list.splice(list.length - 2, 1); //sterge penultimul element si refa array-ul
    }
    //urmatoarele 4 linii nu ar fi necesare pt ca in sortare ceva e dubios đź?®
    if(list.length>=3)
	{
		if (viraj(list[list.length - 2], list[list.length - 1], list[0]) <= 0)
			list.splice(list.length - 1, 1);
		if (viraj(list[list.length - 1], list[0], list[1]) <= 0)
			list.splice(0, 1);
	}
    return list;
}
function viraj(p, q, r) {//<0 in dreapta || >0 in stanga
    var rez1 = (q.x - p.x) * (r.y - p.y);
    var rez2 = (q.y - p.y) * (r.x - p.x);
    return rez1 - rez2;
}
function dist_polara(x) {
    return Math.sqrt(x.x * x.x + x.y * x.y);
}

function sort(v, bar) { //dupa unghiul polar si distanta polara
    var ok = 1;
    while (ok) {
        ok = 0;
        for (var i = 0; i < v.length - 1; i++) {

            var u1 = Math.atan2(v[i].y, v[i].x) * 180 / Math.PI + 180; //ca sa dea in intervalul 0-360
            var u2 = Math.atan2(v[i + 1].y, v[i + 1].x) * 180 / Math.PI + 180;

            
            if (u1 > u2) {
                var aux = v[i + 1];
                v[i + 1] = v[i];
                v[i] = aux;
                ok = 1;
            } else if (u1 == u2) {
                if (dist_polara(v[i]) > dist_polara(v[i + 1])) {
                    var aux = v[i + 1];
                    v[i + 1] = v[i];
                    v[i] = aux;
                    ok = 1;
                }
            }
        }
    }
}