class CmmnFunc {

    static getDateString(date = new Date(), format = "yyyy-mm-dd hh:mi:ss") {
		var eng = /[a-zA-Z]/;
		if(typeof(date) == "string") {
			format = format.replace(/\|hh24/gi, " hh");
			for(var i = 0; i < date.length; i++){
				format = format.replace(eng, date[i]);
			}
			/*date 문자열과 format 길이가 맞지 않는 경우*/
			if(format.search(eng) != -1) format = format.substr(0, format.search(eng) - 1);
			return format;
		}
			
		const yy = date.getFullYear();
		const mm = this.addZero(date.getMonth() + 1);
		const dd = this.addZero(date.getDate());
		const hh = this.addZero(date.getHours());
		const mi = this.addZero(date.getMinutes());
		const ss = this.addZero(date.getSeconds());
			
		format = format.replace("yyyy", yy);
		format = format.replace("mm", mm);
		format = format.replace("dd", dd);
		format = format.replace("hh", hh);
		format = format.replace("mi", mi);
		format = format.replace("ss", ss);
			
		return format;
	}
    
    /*남은 자리 수 만큼 0 채우기 (기본 값 = 2)*/
    static addZero(data, len = 2) {
		const dlen = String(data).length;
		return (dlen >= len ? data : new Array(len - dlen + 1).join("0") + data);
    }
}

// // output : 2022-04-06 16:40:30

// console.log(CmmnFunc.getDateString("20200406"))
// console.log(CmmnFunc.getDateString("2020/04/06"))






// console.log("20200406 => " + type3("20200406"))
// console.log("04-06-2021 => " + type3("04-06-2021"))

// console.log("04-06-2021 => " + type1("04-06-2021"))
// console.log("2022/10/11 => " + type1("2022/10/11"))
// console.log("11/11/2022 => " + type2("11/11/2022"))

var arr = ["2010/02/20", "19/12/2016", "11-18-2012", "20130720", "13-18-2012"];
transformDateFormat(arr);

function transformDateFormat(dates) {
  
    var res = [];
    for(var i=0; i<dates.length; i++) {
      var date = dates[i];
      var y = "";
      var m = "";
      var d = "";
      if(type1(date)) {
        var strArr = date.split("/");
        y = strArr[0];
        m = strArr[1];
        d = strArr[2];       
        if(yearValidate(y) && monthValidate(m) && dayValidate(d)) {
            var commonFormated = y + m + d;
            res.push(commonFormated) 
        }
      } else if(type2(date)) {
        var strArr = date.split("/");
        y = strArr[2];
        m = strArr[1];
        d = strArr[0]; 
        if(yearValidate(y) && monthValidate(m) && dayValidate(d)) {
            var commonFormated = y + m + d;
            res.push(commonFormated) 
        }
      } else if(type3(date)) {
        var strArr = date.split("-");
        y = strArr[2];
        m = strArr[0];
        d = strArr[1]; 
        if(yearValidate(y) && monthValidate(m) && dayValidate(d)) {
            var commonFormated = y + m + d;
            res.push(commonFormated) 
        }
      } else if(date.length == 8) {
        y = date.slice(0, 5);
        m = date.slice(5, 7);
        d = date.slice(7, 9);
      }
      
    }
    console.log(res)
    return res;
}

function yearValidate(year) {
    year = parseInt(year);
    if(year == 0) {
      return false;
    }  
    return true;
}
function monthValidate(month) {
    month = parseInt(month);
    console.log("month"+month)
    if(month > 12 || month == 0) {
        return false;
    }  
    return true;
}
function dayValidate(day) {
    day = parseInt(day);
    console.log("day"+day)
    if(day > 31 || day == 0) {
        return false;
    }  
    return true;
}

function type3(args) {	    
    if (/^[0-9]{2}-[0-9]{2}-[0-9]{4}/.test(args)) {
        return true;
    }
    return false;
}

function type2(args) {	    
    if (/^[0-9]{2}\/[0-9]{2}\/[0-9]{4}/.test(args)) {
        return true;
    }
    return false;
}

function type1(args) {	    
    if (/^[0-9]{4}\/[0-9]{2}\/[0-9]{2}/.test(args)) {
        return true;
    }
    return false;
}