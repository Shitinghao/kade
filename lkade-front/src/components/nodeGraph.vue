<template>
  <div>
    <h1>this is nodeGraph</h1>
    <!--检索实体-->
    <el-input type="text" placeholder="搜索" suffix-icon="el-icon-search" style="width:80%" @keyup.enter.native="search_entity(null)"></el-input>
    <el-button @click="search_entity(null)">搜索</el-button>
    <!--内容展示区-->
    <el-container>
      <el-main>
        <el-row :gutter="20" style="border: 1px solid red;">
          <!--图形控件区-->
          <div style="border: 1px solid black;">
            <el-button type="text" @click="table = true">实体详情</el-button>
          </div>
          <!--graph-->
          <div class="left_graph" ref="left_graph">
          </div>
        </el-row>
      </el-main>
    </el-container>

    <el-drawer
      title="我嵌套了表格!"
      :visible.sync="table"
      direction="rtl"
      size="50%">
      <el-table :data="gridData">
        <el-table-column property="date" label="日期" width="150"></el-table-column>
        <el-table-column property="name" label="姓名" width="200"></el-table-column>
        <el-table-column property="address" label="地址"></el-table-column>
      </el-table>
    </el-drawer>

  </div>

</template>

<script>
  import * as d3 from 'd3'
  export default {
    name: "nodeGraph",
    data() {
      return {
        table: false,
        dialog: false,
        loading: false,
        gridData: [{
          date: '2016-05-02',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄'
        }, {
          date: '2016-05-04',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄'
        }, {
          date: '2016-05-01',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄'
        }, {
          date: '2016-05-03',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄'
        }],
        formLabelWidth: '80px',
        url1:'',
        url2:''
        
      };

    },
    methods: {
      handleClose(done) {
        this.$confirm('确定要提交表单吗？')
          .then(_ => {
            this.loading = true;
            setTimeout(() => {
              this.loading = false;
              done();
            }, 2000);
          })
          .catch(_ => {});
      }
    },
    mounted() {
      var width =window.innerWidth;
      var height =window.innerHeight;
      var nodes = [
          {id:0,name:"哥尔·D·罗杰",info:"海贼王，罗杰海贼团船长，能倾听万物的声音。火拳艾斯的父亲，目前只提到掌握着霸王色“霸气”，拥有“古代兵器”之一“冥王”的能力。与白胡子、金狮子等等大海贼数次交手，唯一得到“one piece”的人，开创了“大海贼时代”，实力理当最强！"},
          {id:1,name:"蒙奇·D·卡普",info:"海军英雄卡普，唯一能把罗杰数次逼入绝境之人。掌握三色霸气，三大将中的青稚曾是他的跟班，至于军衔是卡普本人不贪图名利，中将的军衔已经能够使他任意的出入任何场所，所以他力荐比自己更适合做元帅的老友战国。在大事件中尽管自己非常不情愿参战，可面对“不死鸟马尔克”时，仅一招就将其击倒！"},
          {id:2,name:"爱德华·纽杰特",info:"四皇之一，白胡子海贼团船长，世界最强的男人，最接近海贼王的男人，罗杰的竞争对手，震震果实的能力拥有者，   并掌握了三色霸气。在大事件中身体不适的他，又意外的被“大涡蜘蛛·斯库亚德”刺重身躯，可是在这种状况之下面对三大将赤犬之时，一招就将其击倒，险些毙命，可见实力超乎寻常。"},
          {id:3,name:"费舍尔·泰格",info:"太阳海贼团船长泰格，鱼人岛的大英雄。白胡子与冥王雷利的老友，和白胡子共同保护着鱼人岛，被七武海甚平及鱼人阿隆等人尊为大哥，捣毁了天龙人的圣地玛丽乔亚，解救了包括女帝波雅·汉库克和少女克尔拉在内的所有“奴隶”！"},
          {id:4,name:"金狮子·史基",info:"飞天海贼，金狮子海贼舰队提督，二刀流剑士，飘飘果实能力拥有者。持有的两把名剑“樱十”和“枯木”。过去曾与罗杰和白胡子齐名，传说中使人闻风丧胆的大海贼。多次与罗杰交手。最后与卡普、战国激烈对决后战败，被囚禁在推进城，也是唯一一位从推进城成功逃脱出来的海贼。"},
          {id:5,name:"西尔巴兹·雷利",info:"罗杰海贼团副船长，冥王雷利。可使用三色“霸气”，拥有“霸王色霸气的男人”。面对三大将黄猿之时，虽年纪与体力不如对方，可任在未发动霸气的情况下，持剑挡住了黄猿。大事件后收路飞为徒，传授路飞“霸气”正确使用方法。"},
          {id:6,name:"蒙奇·D·多拉格",info:"革命军首领、世界上最恶的犯罪者，海军英雄卡普的儿子，路飞的父亲。拥有三色“霸气”之人，果实能力说法有两种：1.自然系.暴风果实能力拥有者。2.幻兽种.青龙果实能力拥有者。另外很有可能掌握者“古代兵器”之一“天王”能力拥有者。“天王”拥有毁灭世界的力量，掌握一切天气变化。曾从斯摩格手中放走路飞，理由是“有什么理由阻止一个男人奔向大海”！"},
      ];
      var edges = [
          {source:nodes[0],target:nodes[1],detail:"父节点为0"},
      //      {source:nodes[0],target:nodes[6],detail:"父节点为0"},
      //      {source:nodes[0],target:nodes[3],detail:"父节点为0"},
          {source:nodes[1],target:nodes[4],detail:"父节点为1"},
          {source:nodes[1],target:nodes[6],detail:"父节点为1"},
          {source:nodes[1],target:nodes[3],detail:"父节点为1"},
          {source:nodes[1],target:nodes[2],detail:"父节点为1"},
          {source:nodes[1],target:nodes[5],detail:"父节点为1"},
      //      {source:nodes[5],target:nodes[0],detail:"父节点为5"},
      //      {source:nodes[2],target:nodes[3],detail:"父节点为2"},
      ];
      
      var i = 0,
          duration = 750,//过渡时间
        root;

      var svg = d3.select('body')
        .append('svg')
        .attr('width',width)
        .attr('height',height);

      var force = d3.layout.force()
        .nodes(nodes)            //设定节点数组
        .links(edges)            //设定连线数组
        .size([width,height])    //设定作用范围
        .linkDistance(90)        //设定连线的距离
        .charge(-1600)           //设定节点的电荷数

      force.start();       //开启布局计算

      var updateLine = svg.selectAll(".forceLine")
        .data(edges)
      var enterLine = updateLine.enter();
      var exitLine = updateLine.exit();

      updateLine.attr({
          'd': function(d) {return 'M '+d.source.x+' '+d.source.y+' L '+ d.target.x +' '+d.target.y},
          "class":"forceLine",
          "id":function(d,i){return 'edgepath'+ i;}
      })
          .attr("stroke",'rgb(136,228,179)')
          .attr("stroke-width","1px")
          .attr("marker-end", "url(#resolved)" );

      enterLine.append("path")
          .attr({
              'd': function(d) {return 'M '+d.source.x+' '+d.source.y+' L '+ d.target.x +' '+d.target.y},
              "class":"forceLine",
              "id":function(d,i){return 'edgepath'+ i;}
          })
          .attr("stroke",'rgb(136,228,179)')
          .attr("stroke-width","1px")
          .attr("marker-end", "url(#resolved)" );
      exitLine.remove();
      //绘制连线上的文字
    var updateLineText = svg.selectAll(".forcrLineText")
        .data(edges)
    var enterLineText = updateLineText.enter();
    var exitLineText = updateLineText.exit();

    updateLineText.attr({
        'class':'forcrLineText',//定义该text标签class为forcrLineText
        'id':function(d,i){return 'edgepath'+i;}, //设置id
        'dx':60,           //在连线上的坐标
        'dy':0
    })

    enterLineText.append("text")
        .attr({
            'class':'forcrLineText',//定义该text标签class为edgelabel
            'id':function(d,i){return 'edgepath'+i;}, //设置id
            'dx':60,           //在连线上的坐标
            'dy':0
        })
        .append('textPath')    //设置文字路径
        .attr('xlink:href',function(d,i) {return '#edgepath'+i})
        .style("pointer-events", "none")
        .attr("dy", ".35em") //将文字下移
        .style("font-size", "10px")
        .on("click",function(node){
            updateLine.style("stroke-width",function(line){
                if(line.source.name==node.name || line.target.name==node.name){
                    return 3;//当连接时边+粗
                }else{
                    return 2;
                }
            });
            //所有的圆圈边框
            updateCircle.style('stroke-width',2);
            //被选中的圆圈边框
            d3.select(this).style('stroke-width',4);
        })
        .text(function(d){return d.detail;}); //绘制文字

    exitLineText.remove();


    //绘制节点
    var updateCircle = svg.selectAll(".forceCircle")
        .data(nodes)
    var enterCircle = updateCircle.enter();
    var exitCircle = updateCircle.exit();

    updateCircle.attr("class","forceCircle")
        .attr("r",20)
        .style("fill",'rgb(136,228,179)')
        .style("stroke",'rgb(88,159,175)')
        .style("stroke-width",2)
        .call(force.drag); //允许拖动

    enterCircle.append("circle")
        .attr("class","forceCircle")
        .attr("r",20)
        .style("fill",'rgb(136,228,179)')
        .style("stroke",'rgb(88,159,175)')
        .style("stroke-width",2)
        .on('dblclick',function(d,node){
            d.fixed = false;
            var circle = d3.select(this);
            if(removeNode == true){
                removeNodeData(d,circle);
            }

        })
        .on("click",function(node){
            clickDown = true;
            updateLine.style("stroke-width",function(line){
                if(line.source.name==node.name || line.target.name==node.name){
                    return 3;//当连接时边+粗
                }else{
                    return 1;
                }
            });
            d3.select("#contInfoBox")
                .style({
                    "display":"block",
                });
            d3.select(".contInfo").html(
                '<div><h4>'+node.name+'</h4>' + '<div style="text-indent:2em">'+ node.info +'</div></div>');
            //所有的圆圈边框
            updateCircle.style('stroke-width',2);
            //被选中的圆圈边框
            d3.select(this).style('stroke-width',4);
            //选中状态之后按键删除
            var circle = d3.select(this);
            keydown(node,circle);

        })
        .on("mouseover",function(d){
            //节点的tooltip
            console.log(clickDown)
            if(removeNode == false || clickDown == false ){
                tooltip.html('<div style="border:1px solid cadetblue;border-radius: 5px;background: white;width: 300px;padding:0 0 4px 4px" ><h4>'+d.name+'</h4>' + '<div style="text-indent:2em">'+ d.info +'</div></div>')
                    .style("left", (d3.event.pageX) + "px")
                    .style("top", (d3.event.pageY + 20) + "px")
                    .style("opacity",1.0);
            }else{
                return false;
            }


        })
        .on("mousemove",function(d){
            tooltip.style("left", (d3.event.pageX) + "px")
                .style("top", (d3.event.pageY + 20) + "px");

        })
        .on("mouseout",function(d){
            tooltip.style("opacity",0.0);

        })
        .call(force.drag); //允许拖动
      exitCircle.remove();
      //绘制文字
    var updateText = svg.selectAll(".forceText")
        .data(nodes)
    var enterText = updateText.enter();
    var exitText = updateText.exit();

    updateText.attr("class","forceText")
        .attr("x",function(d){return d.x;})
        .attr("y",function(d){return d.y;})
        .attr("dy",".3em")
        .attr("text-anchor", "middle")
        .text(function(d){return d.name})

    enterText.append("text")
        .attr("class","forceText")
        .attr("x",function(d){return d.x;})
        .attr("y",function(d){return d.y;})
        .attr("dy",".3em")
        .attr("text-anchor", "middle")
        .text(function(d){return d.name})
        .on("click",function(d,i){
            if(editNode == true){
                $("#edit").css({
                    "display":"block",
                    "top":$(this).attr('y') + "px",
                    "left":$(this).attr('x')+ "px",
                });
                $("#edit input").val(d.name);
                //点击事件
                $("#edit button").unbind('click');
                $("#edit button").unbind('click').click(function(){
                    //1、判断是否输入值
                    if($('#edit input').val().length == 0){
                        alert('请输入节点名称');
                        return false;
                    }else{
                        //2.存在输入值
                        //3.确认输入的值是不是存在
                        //判断该节点名是不是已经存在
                        var isNode = false;
                        nodes.filter(function(d,i){
                            if($('#edit input').val() == d.name){
                                alert("该节点名已经存在");
                                isNode = true;
                            }else{
                                index = null;
                            }
                        });
                        //4.如果输入的值存在，则返回false
                        if(isNode == true){
                            return false;
                        }else{
                            //如果不存在，进行编辑替换
                            d.name = $('#edit input').val();
                            svg.selectAll(".forceText")
                                .text(function(d){return d.name})
                            $("#edit").css('display',"none");
                        }

                    }

                });
                //键盘事件
                $("#edit input").unbind('keydown');
                $("#edit input").unbind('keydown').keydown(function (event) {
                    //内部判断start
                    if (event.keyCode == 13) {
                        if($('#edit input').val().length == 0){
                            alert('请输入节点名称');
                            return false;
                        }else{
                            //2.存在输入值
                            //3.确认输入的值是不是存在
                            //判断该节点名是不是已经存在
                            var isNode = false;
                            nodes.filter(function(d,i){
                                if($('#edit input').val() == d.name){
                                    alert("该节点名已经存在");
                                    isNode = true;
                                }else{
                                    index = null;
                                }
                            });
                            //4.如果输入的值存在，则返回false
                            if(isNode == true){
                                return false;
                            }else{
                                //如果不存在，进行编辑替换
                                d.name = $('#edit input').val();
                                svg.selectAll(".forceText")
                                    .text(function(d){return d.name})
                                $("#edit").css('display',"none");
                            }

                        }
                    }
                    //内部判断end
                })
            }
        });

    exitText.remove();

    //tooltip
    var tooltip = d3.select("body")
        .append("div")//添加div并设置成透明
        .attr("class","tooltip")
        .style("opacity",0.0);

    force.on("tick",function(){
        // 跟新连线端点坐标
//          updateLine.attr("x1",function(d){return d.source.x});
//          updateLine.attr("y1",function(d){return d.source.y});
//          updateLine.attr("x2",function(d){return d.target.x});
//          updateLine.attr("y2",function(d){return d.target.y});

//          edges_line.attr("x1",function(d){return d.source.x});

        updateLine.attr('d', function(d) { //连接线
            var path='M '+d.source.x+' '+d.source.y+' L '+ d.target.x +' '+d.target.y;
            return path;
        });

        updateLineText.attr('transform',function(d,i){//连线上的文字
            if (d.target.x<d.source.x){//判断起点和终点的位置，来让文字一直显示在线的上方且一直是正对用户
                let bbox = this.getBBox();//获取矩形空间,并且调整翻转中心。（因为svg与css中的翻转不同，具体区别可看http://www.zhangxinxu.com/wordpress/2015/10/understand-svg-transform/）
                let rx = bbox.x+bbox.width/2;
                let ry = bbox.y+bbox.height/2;
                return 'rotate(180 '+rx+' '+ry+')';
            }
            else {
                return 'rotate(0)';
            }
        })
            .attr('dx',function(d,i){

                return Math.sqrt(Math.pow(d.target.x-d.source.x,2)+Math.pow(d.target.y-d.source.y,2))/2-20;
                //设置文字一直显示在线的中间

            });

        // 跟新节点坐标
        updateCircle.attr("cx",function(d){return d.x});
        updateCircle.attr("cy",function(d){return d.y});
//          enterCircle.attr("cx",function(d){return d.x});
//          enterCircle.attr("cy",function(d){return d.y});

        // 更新节点的文字的坐标
        updateText.attr("x",function(d){return d.x;});
        updateText.attr("y",function(d){return d.y;});
    });


    //拖拽
    var drag = force.drag()
        .on("dragstart",function(d){d.fixed = true;})
        .on("dragend",function(d,i){
            d3.select(this).style({
                "fill":'rgb(136,228,179)',
                "stroke":'rgb(88,159,175)'
            });
//              d.fixed = false;
        })
        .on("drag",function(d){
            d3.select(this).style("fill","rgb(136,228,179)");
        });
    }
  }

</script>

<style scoped>

</style>
