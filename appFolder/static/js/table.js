var userid = $("#userid")[0].textContent;
console.log(userid);
function dispTable(userid){
    $.ajax({
         type: "GET",
         url: "http://127.0.0.1:5000/getUserActivity/"+userid,
         contentType : "application/json",
         success : function(data){
            console.log(data);
            var table = "<table><tr><th>Activity</th><th>Message</th><th>Timestamp</th></tr>";
            for(var i=0; i<data.activities.length; i++){
             table+="<tr>";
             table+="<td>"+data.activities[i][0].activity+"</td>";
             table+="<td>"+data.activities[i][1].message+"</td>";
             table+="<td>"+data.activities[i][2].timestamp+"</td>";
             table+="</tr>"
            }
            table+="</table>"
            $("#tablediv").html(table);
         }
    });

}

dispTable(userid);
$("#mybutton").on("click", function(){
dispTable(userid);
});
