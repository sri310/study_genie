$.ajax({
         type: "GET",
         url: "http://127.0.0.1:5000/bardata",
         contentType : "application/json",
         success : function(data){
         console.log(data);

         var myChart =  echarts.init($("#grouped_bar")[0]);
        console.log(myChart);
        myChart.title = 'Upvote/DownVote';

        option = {
            tooltip : {
                trigger: 'axis',
                axisPointer : {
                    type : 'shadow'
                }
            },
            legend: {
                data:['Upvote', 'DownVote']
            },
            grid: {
                left: '3%',
                right: '8%',
                bottom: '3%',
                containLabel: true
            },
            toolbox: {
            show: true,
            orient: 'vertical',
            left: 'right',
            top: 'center',
            feature: {
                dataView: {show: true, readOnly: false},
                magicType: {show: true, type: ['stack', 'tiled']},
                restore: {show: true},
                saveAsImage: {show: true}
            }
            },
            xAxis : [
                {
                    type : 'value'
                }
            ],
            yAxis : [
                {
                    type : 'category',
                    axisTick : {show: false},
                    data : ['aaa','bbb','ccc']
                }
            ],
            series : [
                {
                   name : 'Upvote',
                    type:'bar',
                    label: {
                        normal: {
                            show: true,
                            position: 'inside'
                        }
                    },
                    data: data.votes[0]
                },
                {
                    name:'DownVote',
                    type:'bar',
                    stack: '总量',
                    label: {
                        normal: {
                            show: true
                        }
                    },
                    data: data.votes[1]
                }
            ]
        };
        myChart.setOption(option);
                 }
})