<template>
  <div>
    <!--<h1>this is nodeGraph</h1>-->
    <!--检索实体-->
    <!--<el-button type="text" @click="table = true">实体详情</el-button>-->
    <!--<el-input type="text" placeholder="搜索" suffix-icon="el-icon-search" style="width:80%" @keyup.enter.native="search_entity(null)"></el-input>-->
    <!--<el-button @click="search_entity(null)">搜索</el-button>-->
    <!--&lt;!&ndash;内容展示区&ndash;&gt;-->
    <!--<el-container>-->
    <!--<el-main>-->
    <!--<el-row :gutter="20" style="border: 1px solid red;">-->
    <!--&lt;!&ndash;图形控件区&ndash;&gt;-->
    <!--<div style="border: 1px solid black;">-->
    <!--&lt;!&ndash;<el-button type="text" @click="table = true">实体详情</el-button>&ndash;&gt;-->
    <!--</div>-->
    <!--&lt;!&ndash;graph&ndash;&gt;-->
    <!--<div class="left_graph" ref="left_graph">-->
    <!--</div>-->
    <!--</el-row>-->
    <!--</el-main>-->
    <!--</el-container>-->

    <el-drawer title="我嵌套了表格!"
               :visible.sync="table"
               direction="rtl"
               size="50%">
      <el-table :data="gridData">
        <el-table-column property="date" label="日期" width="150"></el-table-column>
        <el-table-column property="name" label="姓名" width="200"></el-table-column>
        <el-table-column property="address" label="地址"></el-table-column>
      </el-table>
    </el-drawer>
    <!--<el-card class="box-card">-->
    <div id="edit" class="edit">
      <input type="text" name="" id="words" class="words" autofocus="autofocus" value="" />
    </div>
    <nav class="navbar navbar-inverse" style="background: rgb(113,118,244);border:none;border-radius: 0px;">
      <div class="container-fluid" style="margin-left: 85px;">
        <div class="navbar-header">
          <span style="line-height:50px;margin-top: 20px;">
            <router-link class="nav-item" to="/list">列表</router-link>
            <router-link class="nav-item" to="/nodeGraph">nodeGraph</router-link>
            <!--<span  class=" nodeGraph" href="#" style="color: white;">检索</span>-->
            <!--<router-link class="nav-item nodeGraph" href="#" style="color: white;">检索</router-link>-->
          </span>
          <span>
            <a class="navbar-brand nodeGraph" href="#" style="color: white;">检索</a>
          </span>
        </div>
        <div style="margin-top:14px;">
          <button class="detailEdit btn btn-link btn-self">详情</button>
          <button class="detailEditModal btn btn-link btn-self" data-toggle="modal" data-target="#myModal">详情MODAL</button>
          <form action="" role="form" id="Search" style="display: none;">
            <div class="form-group">
              <input type="text" class="form-control input-sm" placeholder="请输入节点信息">
            </div>
          </form>

        </div>
      </div>
    </nav>
    <!--<div class="container">-->
    <div class="left_graph col-xs-12">
      <!--nodegraph-->
    </div>
    <div class="right_info col-xs-12 "
         style="border-left:1px solid cornflowerblue;
            display: none;
            ">
      <h5 class="text-right info_close" style="margin-bottom: 20px;"><a href="javascript:void(0)">close</a></h5>
      <h4 class="text-center">节点详情</h4>
      <div class="container" style="width: 100%;margin-top:20px;">
        <form role="form">
          <div class="form-group">
            <div style="margin: 10px;">
              <label for="name">节点名称</label>
              <input type="text" id="name"
                     class="form-control"
                     disabled="disabled"
                     placeholder="请输入节点名称">
            </div>
            <div style="margin: 10px;">
              <label for="name">节点信息</label>
              <div id="tableBox" style="width: 100%;overflow: scroll;">
                <table class="table">
                  <thead>
                    <tr>
                      <th>P</th>
                      <th>O</th>
                    </tr>
                  </thead>
                  <tbody id="c_info"></tbody>
                </table>
              </div>
            </div>

          </div>
        </form>
        <div class="footer text-right">
          <button type="button"
                  id="editMore"
                  class="btn btn-info">
            更改
          </button>
          <button type="button"
                  id="subEdit"
                  class="btn btn-primary"
                  data-dismiss="modal"
                  style="background: rgb(136,228,179);">
            提交
          </button>
        </div>

      </div>

    </div>

    <el-dialog title="新增实体" :visible.sync="entDialogVisible" width="50%" :before-close="handleClose">
      <label for="" style="float: left;">name:</label>
      <el-input type="text" v-model="ent_inserts.ename" placeholder="请输入新增实体的名称"></el-input>
      <span slot="footer" class="dialog-footer">
        <el-button @click="entDialogVisible=false">取 消</el-button>
        <el-button type="primary" @click="submitNewEntity">确 定</el-button>
      </span>
    </el-dialog>

    <el-dialog title="显示实体" :visible.sync="showEntDialogVisible" width="50%" :before-close="handleClose">
      <label for="" style="float: left;">name:</label>
      <el-autocomplete v-model="ent_select.eid"
                       :fetch-suggestions="objectSuggestion"
                       placeholder="请输入需要显示实体的名称"></el-autocomplete>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showEntDialogVisible=false">取 消</el-button>
        <el-button type="primary" @click="showEntity">确 定</el-button>
      </span>
    </el-dialog>

    <!--modal-->
    <!-- 模态框（Modal） -->
    <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
              &times;
            </button>
            <h4 class="modal-title" id="myModalLabel"></h4>
          </div>
          <div class="modal-body">
            <div><span>P:</span><span contenteditable="true">O</span></div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">
              关闭
            </button>
            <button type="button" class="btn" style="background: rgb(113,118,244);color: white;">
              提交更改
            </button>
          </div>
        </div><!-- /.modal-content -->
      </div><!-- /.modal -->
    </div>
    <!--</el-card>-->
  </div>

</template>

<script>
  import * as d3 from 'd3'
  import global from './nav.vue'
  // import
  export default {
    name: "nodeGraph",
    data() {
      return {
        api_host: global.api_host,
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
        url2: '',
        showEntDialogVisible: false,
        entDialogVisible: false,
        ent_select: { ename:"", eid: "", options:[]},
        ent_inserts: { ename: '' },
      };

    },
    methods: {
      handleClose(done) {
        return done();
        this.$confirm('确定要提交表单吗？')
          .then(_ => {
            this.loading = true;
            setTimeout(() => {
              this.loading = false;
              done();
            }, 2000);
          })
          .catch(_ => {});
      },
      checkAndSubmit(_this, url, pparams, succ_func, fail_func) {
        pparams["precheck"] = 1
        _this.axios
          .get(url, {
            params: pparams
          })
          .then(function (response) {
            if (response.data.status !== "ok") {
              fail_func(response, _this)
            } else {
              delete pparams["precheck"];
              _this.axios
                .get(url, {
                  params: pparams
                })
                .then(response => succ_func(response, _this))
                .catch(function (error) {
                  console.log(error);
                });
            }
          })
          .catch(function (error) {
            console.log(error);
          });
      },
      submitNewEntity() {
        let _this = this;
        this.checkAndSubmit(this, this.api_host+'/api/new_entity', {
              name: this.ent_inserts.ename
          },
          function (response, _this) {
            let ename = _this.ent_inserts.ename;
            _this.ent_inserts.ename = "";
            _this.entDialogVisible = false;
            _this.svg.classed('active', true);

            // insert new node at point
            let point = _this.ent_inserts.point;
            let timest = _this.ent_inserts.timest;
            let node = {id: ++_this.lastNodeId, idx:ename ,name:ename, reflexive: false, info:[{idx:"xx",o:"xx",p:"xx",s:"xx",timeStamp:timest}]};
            node.x = point[0];
            node.y = point[1];
            _this.nodes.push(node);

            _this.restart();
          },
          function (response, _this) {
            _this.$message.error(response.data.msg);
          }
        )
      },

      objectSuggestion(query, cb) {
        let _this = this;
        this.axios
          .get(_this.api_host+'/api/ment2ent', {
            params: {
              q: query,
              no_other_m: 1
            }
          })
          .then(function (response) {
            let ents = response.data.ret;
            let ent_select = JSON.parse(JSON.stringify(_this.ent_select)); //deepcopy
            ent_select.options = [];
            ents.forEach(function (x) {
              ent_select.options.push({
                link: x.ename,
                value: x.eid
              });
            });
            _this.ent_select = ent_select.options;
            cb(ent_select.options);
          })
          .catch(function (error) {
            console.log(error);
          });
      },
      showEntity() {
        console.log(this.ent_select.eid);
      }
    },
    mounted() {
      var _this = this;
      var width = $('.left_graph').width(),
      height = window.innerHeight-79 ,
      colors = d3.scale.category10();

      var svg = d3.select('.left_graph')
        .append('svg')
        .attr('class','layout')
        .attr('width', width)
        .attr('height', height);

      var nodes = [];
      var links = [];
      var searchWords = global.main_entity;
      var inputEdit = true;
      var state_r = false;
      var state_l = false;
      var state_u = false;
      var state_d = false;
      var max_x = null;
      var max_y = null;
      var min_x = null;
      var min_y = null;
      var selected = '';//全局的node
      var edit_relation = false;
      var click_edit = false;
      var api_host = _this.api_host;

      _this.nodes = nodes;
      _this.svg = svg;
      _this.lastNodeId = null;

// mouse event vars
      var selected_node = null,
        selected_link = null,
        selected_link_text = null,
        mousedown_link = null,
        mousedown_link_text = null,
        mousedown_node = null,
        mouseup_node = null;
      var tooltip = d3.select("body")
        .append("div")//添加div并设置成透明
        .attr("class","tooltip")
        .style("opacity",0.0);

      start();
      function start(){
        $.get(api_host+"/api/graph/query_entity?idx="+ searchWords, function (response) {
          response = JSON.parse(response);
          console.log(response);
          if(response.status == "success"){
            console.log("检索成功");
          }else{
            alert("查询失败，请重新输入查询词");
          }
          _this.lastNodeId = response.nodes.length-1;
          $.each(response.nodes, function(i,val) {
            nodes.push({id:i, idx:val.idx, name:val.idx, reflexive:false, info:val.attr});
          });
          $.each(response.links,function(i,val){
            var id = val.source;
            var tid = val.target;
            links.push({source:nodes[id],target:nodes[tid],left:false,right:true,relation:val.triple.p,triple:val.triple});
          })
          console.log('nodes:');
          console.log(nodes);
          console.log('links:');
          console.log(links);

// init D3 force layout
          var force = d3.layout.force()
            .nodes(nodes)
            .links(links)
            .size([width, height])
            .linkDistance(150)
            .charge(-500)
            .on('tick', tick);

          _this.force = force;

// define arrow markers for graph links
          svg.append('svg:defs').append('svg:marker')
            .attr('id', 'end-arrow')
            .attr('viewBox', '0 -5 10 10')
            .attr('refX', 6)
            .attr('markerWidth', 5)
            .attr('markerHeight', 5)
            .attr('orient', 'auto')
            .append('svg:path')
            .attr('d', 'M0,-5L10,0L0,5')
            // .attr('fill', 'rgb(113,118,244)');
            .attr('fill','lavender');

          svg.append('svg:defs').append('svg:marker')
            .attr('id', 'start-arrow')
            .attr('viewBox', '0 -5 10 10')
            .attr('refX', 4)
            .attr('markerWidth', 5)
            .attr('markerHeight', 5)
            .attr('orient', 'auto')
            .append('svg:path')
            .attr('d', 'M10,-5L0,0L10,5')
            .attr('fill','lavender');
          // .attr('fill', 'rgb(113,118,244)');

// line displayed when dragging new nodes
          var drag_line = svg.append('svg:path')
            .attr('class', 'link dragline hidden')
            .attr('d', 'M0,0L0,0');

// handles to link and node element groups
          var path = svg.append('svg:g').selectAll('path'),
            path_text = svg.append("g").selectAll(".edgelabel"),
            circle = svg.append('svg:g').selectAll('g');



          function resetMouseVars() {
            mousedown_node = null;
            mouseup_node = null;
            mousedown_link = null;
            mousedown_link_text = null;
          }

// update force layout (called automatically each iteration)
          function tick() {
// draw directed edges with proper padding from node centers
            path.attr('d', function(d) {
              var deltaX = d.target.x - d.source.x,
                deltaY = d.target.y - d.source.y,
                dist = Math.sqrt(deltaX * deltaX + deltaY * deltaY),
                normX = deltaX / dist,
                normY = deltaY / dist,
                sourcePadding = d.left ? 17 : 12,
                targetPadding = d.right ? 17 : 12,
                sourceX = d.source.x + (sourcePadding * normX),
                sourceY = d.source.y + (sourcePadding * normY),
                targetX = d.target.x - (targetPadding * normX),
                targetY = d.target.y - (targetPadding * normY);
              return 'M' + sourceX + ',' + sourceY + 'L' + targetX + ',' + targetY;
            });

            circle.attr('transform', function(d) {
              return 'translate(' + d.x + ',' + d.y + ')';
            });
          }

// update graph (called when needed)
          function restart() {

// 1.path
// path (link) group
            path = path.data(links);

// update existing links
            path.classed('selected', function(d) {
              return d === selected_link;
            })
              .style('marker-start', function(d) {
                return d.left ? 'url(#start-arrow)' : '';
              })
              .style('marker-end', function(d) {
                return d.right ? 'url(#end-arrow)' : '';
              });


// add new links
            path.enter().append('svg:path')
              .attr('class', 'link')
              .attr('id',function(d,i){return 'edgepath'+ i;})
              .classed('selected', function(d) {
                return d === selected_link;
              })
              .style('marker-start', function(d) {
                return d.left ? 'url(#start-arrow)' : '';
              })
              .style('marker-end', function(d) {
                return d.right ? 'url(#end-arrow)' : '';
              })
              .style({
                'stroke':'lavender',
                'stroke-width': '2px',
                // ' cursor': 'default'
              })
              .on('mousedown', function(d) {
                if(d3.event.ctrlKey) return;
                // select link
                mousedown_link = d;
                if(mousedown_link === selected_link) selected_link = null;
                else selected_link = mousedown_link;
                console.log("select link");
                console.log(selected_link);
                selected_node = null;
                restart();
              });

// remove old links
            path.exit().remove();

      //2.path text
      // path text(link) group
            path_text = path_text.data(links);

        // update exite path text
            path_text.attr({
              'class':'edgelabel',
              'id':function(d,i){return 'edgepath'+i;},
              'dx':50,
              'dy':0
            });

        // add new path text
            path_text.enter().append("text")
              .attr({
                'class':'edgelabel',
                'id':function(d,i){return 'edgepath'+ i;},
                'dx':50,
                'dy':0
              })
              .append('textPath')
              .attr('xlink:href',function(d,i) {return '#edgepath'+i})
              .style("pointer-events", "auto")
              .attr('class','ptext')
              .text(function(d){return d.relation;})
              .on('mousedown',function(d){
                if(d3.event.ctrlKey) return;
                //设置样式与数据
                mousedown_link_text = d;
                selected = mousedown_link_text;
                $("#edit").css('display','block');
                // $("#words").attr('autofocus','autofocus');
                // console.log($("#words"));
                $('.detailEdit').css('display','none');
                $("#words").val(d.relation);

                edit_relation = true;
                svg.selectAll('.ptext')
                  .style('fill','black')
                d3.select(this).style('fill','blue');
                $("#edit").css({
                  'display':'inline-block',
                  "top":mousedown_link_text.target.y + "px",
                  "left":mousedown_link_text.target.x + "px",
                });

                // console.log(mousedown_link_text);
                if(mousedown_link_text === selected_link_text) selected_link_text = null;
                else selected_link_text = mousedown_link_text;

                console.log("select link 2");
                console.log(selected_link_text);

                selected_node = null;
                $("#words").focus();
                restart();
              })
              .on('mouseup',function (d) {
                $("#edit input").focus();
              });
// remove old pathText
            path_text.exit().remove();

//3.circle
// circle (node) group
// NB: the function arg is crucial here! nodes are known by id, not by index!
            circle = circle.data(nodes, function(d) { return d.id; });

// update existing nodes (reflexive & selected visual states)
            circle.selectAll('circle')
              .style('fill', function(d) {
                return (d === selected_node) ? d3.rgb(150,215,250).brighter().toString() : d3.rgb(150,215,250);
              })
              .classed('reflexive', function(d) { return d.reflexive; });

// add new nodes
            var g = circle.enter().append('svg:g');

            g.append('svg:circle')
              .attr('class', 'node')
              .attr('r', 12)
              //      .attr('r', 8)
              .style('fill', function(d) {
                return (d === selected_node) ? d3.rgb(150,215,250).brighter().toString() : d3.rgb(150,215,250);
              })
              .classed('reflexive', function(d) { return d.reflexive; })
              .on('mouseover', function(d) {
                var html = '';
                var desc = '';
                if(d.info.length == 0){
                  html = '暂无信息';
                }else if(d.info == '暂无信息'){
                  html = '暂无信息';
                }else{
                  $.each(d.info,function(i,val){
                    if(val.p == 'DESC'){
                      if(val.o.length>100){
                        val.o = val.o.substr(0,50)+'...'
                      }
                    }
                    html += '<div><span style="color:blue;">'+val.p+':</span><span>'+val.o+'</span></div>';
                  })
                }

                tooltip.html('<div style="border:1px solid rgb(113,118,244);border-radius: 5px;background: white;width: 400px;padding:0 0 4px 4px" ><h4>'+d.name+'</h4>' + '<div style="text-indent:2em">'+ html +'</div></div>')
                  .style("left", (d3.event.pageX) + "px")
                  .style("top", (d3.event.pageY + 10) + "px")
                  .style("display", 'block')
                  .style("opacity",1.0);

                if(!mousedown_node || d === mousedown_node) return;
                // enlarge target node
                d3.select(this).attr('transform', 'scale(1.1)');
              })
              .on('mouseout', function(d) {
                tooltip.style("opacity",0.0);
                tooltip.style('display','none');
                if(!mousedown_node || d === mousedown_node) return;
                // unenlarge target node
                d3.select(this).attr('transform', '');
              })
              .on('mousedown', function(d) {
                if(d3.event.ctrlKey) return;
                // select node
                mousedown_node = d;

                // d.fixed = false;

                if(mousedown_node === selected_node) selected_node = null;
                else selected_node = mousedown_node;
                selected_link = null;
                //显示info信息
                aboutInfo(selected_node);
                //选中节点后，调用SELECT（）计算4个象限
                //findnode
                if(selected_node == null ){
                  //newResult = findNode(selected_node);
                  //i = 0;
                }else{
                  //关于space的节点遍历
                  newResult = findNode(selected_node);
                  // SELECT(selected_node);
                  i = 0;

                }

                // reposition drag line

                drag_line
                  .style('marker-end', 'url(#end-arrow)')
                  .classed('hidden', false)
                  .attr('d', 'M' + mousedown_node.x + ',' + mousedown_node.y + 'L' + mousedown_node.x + ',' + mousedown_node.y);
                restart();
              })
              .on('mouseup', function(d) {
                if(!mousedown_node) return;
                //因为在mousedown事件比up事件靠前，所以，将focus事件写在mousedown里面不生效（不会执行），mousedown > focus > mouseup > click
                $("#edit input").focus();
                // needed by FF
                drag_line
                  .classed('hidden', true)
                  .style('marker-end', '');

                // check for drag-to-self
                mouseup_node = d;
                if(mouseup_node === mousedown_node) { resetMouseVars(); return; }

                // unenlarge target node
                d3.select(this).attr('transform', '');

                // add link to graph (update if exists)
                // NB: links are strictly source < target; arrows separately specified by booleans
                var source, target, direction;
                if(mousedown_node.id < mouseup_node.id) {
                  source = mousedown_node;
                  target = mouseup_node;
                  direction = 'right';
                } else {
                  source = mouseup_node;
                  target = mousedown_node;
                  direction = 'left';
                }

                var link;
                link = links.filter(function(l) {
                  return (l.source === source && l.target === target);
                })[0];
                console.log(link);

                if(link) {
                  link[direction] = true;
                } else {
                  link = {source:target, target:source ,left: false, right: false,relation:'relation？',triple:{idx:'',o:target.idx,p:'relation?',s:source.idx}}
                  link[direction] = true;
                  links.push(link);
                  var data = {s:target.idx,p:'relation',o_id:source.idx,o_name:source.idx};
                  $.post(api_host+'/api/graph/add_relation', data, function(result){
                    result = JSON.parse(result);
                    link.triple.idx = result.idx;
                  });
                  console.log(links);
                }

                // select new link
                selected_link = link;
                selected_node = null;
                restart();
              });

            // show node IDs
            g.append('svg:text')
            //
              .attr('x', 0)
              //        .attr('y', 4)//-16
              .attr('y',function(d){
                if(d.name == nodes[0].name){
                  return 5
                }else{
                  return -16
                }
              })
              .attr('class', 'id')
              .style({
                'fill': function (d) {
                  if(d.name == nodes[0].name){
                    return 'black'
                  }else{
                    return 'rgb(125,129,128)'
                  }
                }
              })
              .text(function(d) {return  d.name;});

// remove old nodes
            circle.exit().remove();
// set the graph in motion
            force.start();
          } // function restart end

          _this.restart = restart;

          function mousedown() {
            // prevent I-bar on drag
            //d3.event.preventDefault();
            if (d3.event.ctrlKey || mousedown_node || mousedown_link || mousedown_link_text) return;
            var point = d3.mouse(this), timest = new Date().getTime();
            _this.ent_inserts.point = point;
            _this.ent_inserts.timest = timest;
            _this.showEntDialogVisible = true;
            return;
          }

          function mousemove() {
            if(!mousedown_node) return;

            // update drag line
            drag_line.attr('d', 'M' + mousedown_node.x + ',' + mousedown_node.y + 'L' + d3.mouse(this)[0] + ',' + d3.mouse(this)[1]);

            restart();
          }

          function mouseup() {
            $("#edit input").focus();//新增节点聚焦
            if(mousedown_node) {
              // hide drag line
              drag_line
                .classed('hidden', true)
                .style('marker-end', '');
            }

            // because :active only works in WebKit?
            svg.classed('active', false);

            // clear mouse event vars
            resetMouseVars();
          }

          function spliceLinksForNode(node) {
            var toSplice = links.filter(function(l) {
              return (l.source === node || l.target === node);
            });
            toSplice.map(function(l) {
              links.splice(links.indexOf(l), 1);
            });
          }

// only respond once per keydown
          var lastKeyDown = -1;
          var i= 0;
          var newResult = null;
          function keydown() {
//d3.event.preventDefault();//阻止了所有的默认的键盘事件

            if(lastKeyDown !== -1) return;
            lastKeyDown = d3.event.keyCode;

            // ctrl
            if(d3.event.keyCode === 17) {
              circle.call(force.drag);
              svg.classed('ctrl', true);
            }

            if(!selected_node && !selected_link) return;
            switch(d3.event.keyCode) {
//  case 8: // backspace
              case 46: // delete
                if(selected_node) {
                  nodes.splice(nodes.indexOf(selected_node), 1);
                  spliceLinksForNode(selected_node);
                  console.log(selected_node);
                  let ridx = selected_node.idx;
                  $.post(api_host+"/api/graph/delete_entity", {idx:ridx}, function(result){
                    console.log(result);
                    _this.$message("删除实体 " + ridx + " 成功");
                  })
                } else if(selected_link) {
                  links.splice(links.indexOf(selected_link), 1);
                  $.post(api_host+"/api/graph/delete_relation", {idx:selected_link.triple.idx},function(result){
                    console.log(result);
                  })
                }
                selected_link = null;
                selected_node = null;
                //删除节点后，将原本的id换成新的id因为原本的node的自带的索引会自动减少，而元素的id属性不会自动减少，所以需要重新刷新id，否则会报错
                --_this.lastNodeId;
                restart();
                $.each(nodes,function(i,val){
                  val.id = i;
                });
                $("#edit").css('display','none');
                break;

              case 13: //A /enter
                d3.event.preventDefault();
                if (selected_node && inputEdit){

                  var a ='node'+ Math.random()*100;
                  var times = new Date().getTime();
                  var node = {id: ++_this.lastNodeId,idx:a ,name: a , reflexive: false,info:[{idx:"xx",o:"xx",p:"xx",s:"xx",timeStamp:times}]};
                  nodes.push(node);
                  console.log(nodes);
                  // link = {source:target, target:source ,left: false, right: false,relation:'relation？',triple:{idx:'',o:target.idx,p:'relation?',s:source.idx}}

                  var link = {source:nodes[selected_node.id],target:nodes[node.id], left: false, right: true,relation:'relation？',triple:{idx:'',o:node.idx,p:'relation?',s:selected_node.idx}};
                  links.push(link);
                  console.log(link)
                  $.post(api_host+"/api/graph/add_entity?idx=" + a, function (result) {
                    result = JSON.parse(result);
                    console.log(result);
                    if(result.status == 'success'){
                      console.log(result);
                      nodes[node.id].idx = result.idx;
                      data = {
                        sid:link.source.idx,
                        p:'关系？',
                        oid:nodes[node.id].idx,
                      }
                      $.post(api_host+'/api/graph/add_relation',data,function(result){
                        result = JSON.parse(result);
                        if(result.status == 'success'){
                          link.idx = result.idx;
                          console.log(result);
                          return link.idx;
                        }
                      });
                      // console.log(selected_node)
                      $("#edit").css({
                        'display':'inline-block',
                        "top":selected_node.y + "px",
                        "left":selected_node.x+ "px",
                      });
                      $('#edit input').focus();
                      ++_this.lastNodeId;
                      return result.idx;

                    }else{
                      alert('新增节点失败');
                    }
                  });

                  //改变焦点
                  selected_node = nodes[nodes.length-1];
                  //改变焦点的input的val

                  $("#words").val(selected_node.name);

                  selected = selected_node;
                  $('.detailEdit').css('display','block');



                  aboutInfo(selected);
                  console.log(nodes);
                  console.log(links);
                  console.log(_this.lastNodeId);
                  restart();
                }

                break;

              case 66: // B
                if(selected_link) {
                  // set link direction to both left and right
                  //设置连线的方向也就是箭头的方向左和右
                  selected_link.left = true;
                  selected_link.right = true;
                }
                restart();
                break;
              case 76: // L
                if(selected_link) {
                  // set link direction to left only
                  //设置连线的方向也就是箭头的方向左
                  selected_link.left = true;
                  selected_link.right = false;
                }
                restart();
                break;
              case 82: // R
                if(selected_node) {
                  // toggle node reflexivity 取消默认的reflexivity
                  selected_node.reflexive = !selected_node.reflexive;
                } else if(selected_link) {
                  // set link direction to right only
                  //设置连线的方向也就是箭头的方向右
                  selected_link.left = false;
                  selected_link.right = true;
                }
                restart();
                break;

              case 37://left
                if(selected_node){
                  if (SELECT(selected_node).left == undefined){
                    return false;
                  }else{
                    selected_node = SELECT(selected_node).left.data.data;
                    aboutInfo(selected_node);
                  }
                }
                restart();
                break;
              case 38://up target
                if(selected_node){
                  if (SELECT(selected_node).up == undefined){
                    return false;
                  }else{
                    selected_node = SELECT(selected_node).up.data.data;
                    aboutInfo(selected_node)
                  }
                }
                restart();
                break;
              case 39://right
                if(selected_node){
                  if (SELECT(selected_node).right== undefined){
                    return false;
                  }else{
                    selected_node = SELECT(selected_node).right.data.data;
                    aboutInfo(selected_node);
                  }
                }
                restart();
                break;
              case 40://down source
                if(selected_node){
                  if (SELECT(selected_node).down== undefined){
                    return false;
                  }else{
                    selected_node = SELECT(selected_node).down.data.data;
                    aboutInfo(selected_node);
                  }
                }
                restart();
                break;
              case 32://space
                if(selected_node){
                  tabNode(selected_node);
                  if(i<newResult.length){
                    selected_node = newResult[i];
                    aboutInfo(selected_node);
                  }else if(i == newResult.length){
                    i = -1;
                  }
                  i++;
                }
                restart();
                break;
              case 27://esc
                console.log(123);
                if(selected_node){
                  $("#edit").css({'display':'none',});
                }
                restart();
                break;

            }
          }

          function keyup() {
            lastKeyDown = -1;

            // ctrl
            if(d3.event.keyCode === 17) {
              circle
                .on('mousedown.drag', null)
                .on('touchstart.drag', null);
              svg.classed('ctrl', false);
            }
          }

// app starts here
          svg.on('mousedown', mousedown)
            .on('mousemove', mousemove)
            .on('mouseup', mouseup);
          d3.select(window)
            .on('keydown', keydown)
            .on('keyup', keyup);
          restart();
          //    get end
        });
//    function satrt  end
      }


      svg.style('width','100%');
//关于数据的整理
      function tabNode(selected_node){
        var arr_x = [];
        var arr_y = [];
        var arr_x_l = [];
        var arr_x_r = [];
        var arr_y_u = [];
        var arr_y_d = [];
        $.each(nodes, function(i,val) {
          if(val.x<selected_node.x){
            arr_x_l.push(val);
          }
          if(val.x>selected_node.x){
            arr_x_r.push(val);
          }
          if(val.y<selected_node.y){
            arr_y_u.push(val);
          }
          if(val.y>selected_node.y){
            arr_y_d.push(val);
          }
          arr_x.push(val.x);
          arr_y.push(val.y);

        });
        arr_x.sort(d3.ascending);
        arr_y.sort(d3.ascending);
        arr_x_l.sort(d3.ascending);
        arr_x_r.sort(d3.ascending);
        arr_y_u.sort(d3.ascending);
        arr_y_d.sort(d3.ascending);
        max_x = d3.max(arr_x);
        max_y = d3.max(arr_y);
        min_x = d3.min(arr_x);
        min_y = d3.min(arr_y);
        return {x:arr_x,y:arr_y,x_l:arr_x_l,x_r:arr_x_r,y_u:arr_y_u,y_d:arr_y_d};
      }
//计算角度的公式,计算选中节点与所有节点之间的夹角
      function calcAngleDegrees(source_x,source_y,target_x,target_y) {
       var result=Math.atan2(target_y-source_y,target_x-source_x) * 180 / Math.PI;
        if(result>0){
          return result;
        }else{
          return 360+result;
        }
      }
// calcAngleDegrees()
//查找节点
      function findNode(selected_node){
        //查找source与target的节点
        var arr = [];
        //匹配在links中source为选中节点，以及将选中节点作为target的节点
        links.filter(function(x){
          //如果选中节点的idx == links里面的原节点的idx，
          if (selected_node.idx == x.source.idx){
            arr.push(x.target);
            return arr ;
          }
          //或者选中的节点是idx的idx与target的idx相同
          if(selected_node.idx == x.target.idx){
            arr.push(x.source);
          }
        });
        //console.log(arr);//这里会有重复的数据
        //遍历数据，去重
        var newNode = [...new Set(arr)];
        var newResult = [];
        var newresultdata = [];
        //遍历新的选择好的数据
        $.each(newNode,function (i,val) {
          var a = calcAngleDegrees(selected_node.x,selected_node.y,val.x,val.y);
          newresultdata.push({'result':a,'data':val});
        });
        //排序
        newresultdata.sort(sortNumber);
        $.each(newresultdata, function (i,val) {
          newResult.push(val.data);
        })
        //console.log(newResult);
        return newResult;
      }
//排序
      function sortNumber(a,b) {
        return a.result - b.result;
      }

      function SELECT(selected_node){
        //定义选中的4个点
        var up = null;
        var right = null;
        var down = null;
        var left = null;
        var angleNode = [];
        var rightArray = [];
        var downArray = [];
        var leftArray = [];
        var upArray = [];
        //
        $.each(nodes,function(i,val){
          var a = calcAngleDegrees(selected_node.x,selected_node.y,val.x,val.y);
          angleNode.push({'result':a,'data':val})
        });
        // console.log(angleNode);
        $.each(angleNode,function (i,val) {
          if (val.result > 0 && val.result<=45 || val.result > 315 && val.result <360){
            rightArray.push(val);
          }
          if (val.result > 45 && val.result <= 135){
            downArray.push(val);
          }
          if (val.result > 135 && val.result <= 225){
            leftArray.push(val);
          }
          if (val.result > 225 && val.result <= 315){
            upArray.push(val)
          }
        })
        // console.log(rightArray);
        right =  nodeDistance(selected_node , rightArray);
        down = nodeDistance(selected_node , downArray);
        left = nodeDistance(selected_node , leftArray);
        up = nodeDistance(selected_node , upArray);
        return {"selected_node" : selected_node , "right" : right , "down" : down , "left" : left , "up" : up };
        console.log({"selected_node" : selected_node , "right" : right , "down" : down , "left" : left , "up" : up });

      }
//计算两点之间的距离
      function nodeDistance(selected_node,array){
        var distanceArray = [];
        $.each(array,function (i,val) {
          var d = Math.sqrt((selected_node.x - val.data.x)*(selected_node.x - val.data.x) + (selected_node.y - val.data.y)*(selected_node.y - val.data.y) );
          distanceArray.push({'result':d,'data':val});
        });
        distanceArray.sort(sortNumber);
        return distanceArray[0];//返回最小值

      }


      $('#edit_btn').on('click',function(){
        click_edit = true;
      })
//     点击nodeGraph出现检索框
      $('.nodeGraph').on('click', function () {
        $('#Search').fadeToggle();
      });
      $('#Search').on('submit',function(){
        selected_node = null;
        searchWords = $('#Search .form-control').val();
        console.log(searchWords);
        nodes = [];
        links = [];
        _this.lastNodeId = null;
        d3.selectAll("svg>*").remove();
        start();
        $('.left_graph').removeClass('col-md-9');
        $('.right_info').removeClass('col-md-3');

        $('.right_info').css({
          'display':'none',
          'height': ''
        });
        $('#edit').css('display','none')
        return false;
      })
      //输入框聚焦事件，取消默认选中增加的状态
      $('#Search .form-control').focus(function(){
        selected_node = null;
        $("#edit").css("display","none");
      });
      //编辑节点
      function editNode(){
        //获取input的输入值
        var editWords = $("#words").val();
        //判断输入框是否输入东西
        if(editWords.length !== 0){
          //将选中的节点的name赋值为输入框的值
          selected.name = editWords;
          //将选中的relation赋值为输入的值
          selected.relation = editWords;
          //将content的info的input框的值为输入的值
          $("#name").val(editWords);
          //选择所有的节点（节点有class属性id），并将节点的文字全部重新绘制
          svg.selectAll('.id')
            .text(function(selected){return selected.name});
          //发送请求跟新数据库数据;
          $.post('http://47.101.181.52:22222/api/cndbpedia/graph/update_entity',{'idx':selected.idx,'new_id':selected.name},function(result){

            result = JSON.parse(result);
            console.log(result);
            // if(result.status == "success"){
            //     alert('修改节点成功');
            // }else {
            //     alert('修改节点失败');
            // }
          });
          //判断是否是便捷节点的状态

          if(edit_relation==true){
            //选择所有的连线文字，重新绘制文字，并恢复修改后为黑色字体
            svg.selectAll('.ptext')
              .style('fill','black')
              .text(function(selected){return selected.relation});
            //发送数据请求
            console.log(selected.idx);
            console.log(selected.relation);
            $.post(api_host+'/api/graph/update_triple_p',{'idx':selected_link_text.triple.idx,'new_p':selected.relation},function(result){
              console.log(result);
            });
            //修改完成之后再次将修改节点的状态设置为false
            edit_relation = false;
          }
          //修改完成之后，将编辑框影藏
          $('#edit').css('display','none');
          //将详情按钮隐藏
          $('.detailEdit').css('display','none');
          //将详情modal隐藏
          $('.detailEditModal').css('display','none');
        }else{
          alert("请输入节点名");
          return false;
        }
        //如果是在submit的方法中调用会发生页面跳转的bug，所以return false可以避免bug
        return false;
      }


      $('#submit').on('click',function(){
        editNode();
      });
      $('#words').on('keydown',function(e){
        if(e.keyCode == 13){
          editNode();
        }
      });
      //判断input的焦点，来保证是否绑定enter事件
      $('#words').focus(function(){inputEdit = false;});
      $('#words').blur(function(){inputEdit = true;});

      function showInfo(){
        //点击详情 详情出现 nav的输入框不显示
        $('.detailEdit').on('click',function(){
          // console.log(121);
          $('.left_graph').addClass('col-md-9');
          $('.right_info').addClass('col-md-3');

          $('.right_info').css({
            'display':'block',
            'height': height
          });
          $('#tableBox').css({'height':height-250});
//            $('#edit').css('display','none')

        })
        //点击更改
        $('#editMore').on('click',function(){
          $('#name').attr('disabled',false);
          //texteara的信息显示(之前是用来显示info信息的)
//                 $('#nodeInfomation').attr('disabled',false);
          $('.table .Itemlist').attr('contenteditable',true);

        });
        //点击提交
        $('#subEdit').on('click',function(){
          console.log($('#name').val());
          selected.name = $('#name').val();
          console.log(selected);

          console.log($("#c_info .Itemlist").text());
          var itemInfo = []
//                 selected.info = [];
//                 selected.info = itemInfo;
          svg.selectAll('.id')
            .text(function(selected){return selected.name});
          $('#words').val($('#name').val());
          $('#name').attr('disabled',true);

//                    $('#nodeInfomation').attr('disabled',true);
          $('.table .Itemlist').attr('contenteditable',false);
        });
        //点击close
        $('.info_close').on('click',function(){
          $('.left_graph').removeClass('col-md-9');
          $('.right_info').removeClass('col-md-3');

          $('.right_info').css({
            'display':'none',
            'height': ''
          });
          $('#edit').css('display','none')
        })


      }
      showInfo();
      function aboutInfo(selected_node){
        // console.log(selected_node.y);
        // console.log(selected_node.x);

        //显示info信息
        var html = '';
        var html2 = '';
        //判断selected_node的状态，选中还是取消选中
        if(selected_node !== null){
          //如果info没有信息
          if(selected_node.info.length == 0){
            html += '<tr><td class="Itemlist">属性</td><td class="Itemlist">暂无</td></tr>';
            html2 +=  '<div><span style="color:blue;" contenteditable="true">属性:</span><span contenteditable="true">暂无</span></div>';
          }else if(selected_node.info == '暂无信息'){
            html += '<tr><td class="Itemlist">属性</td><td class="Itemlist">暂无</td></tr>';
            html2 +=  '<div><span style="color:blue;" contenteditable="true">属性:</span><span contenteditable="true">暂无</span></div>';
          }else{
            //遍历info中的信息
            jQuery.each(selected_node.info,function(i,val){
              html += '<tr><td class="Itemlist">'+val.p+'</td><td class="Itemlist">'+val.o+'</td></tr>';
              html2 += '<div><span style="color:blue;">'+val.p+':</span><span contenteditable="true">'+val.o+'</span></div>';
            });
          }
          //将信息显示在页面
          $('#c_info').html(html);
          $('.modal-body').html(html2);
          //选中节点后，显示input框在节点周围
          $("#edit").css({
            'display':'inline-block',
            "top":selected_node.y + 30 + "px",
            "left":selected_node.x+ "px",
          });
          // $('#edit input').css('display','block');

          //详情按钮显示
          $('.detailEdit').css('display','block');
          $('.detailEditModal').css('display','block');
          //编辑按钮显示。。。可以删除
          $('#edit_btn').css('display','block');
          //节点跟前的输入框中val赋值
          $("#words").val(selected_node.name);

          //info详情中input的val的赋值
          $("#name").val(selected_node.name);
          $('#myModalLabel').text(selected_node.name);
          //聚焦input
          $("#edit input").focus();
          //节点遍历，该newResult有不规范的时候
        }else{ //取消选中状态 = close
          //整体页面布局
          console.log('close');
          $('.left_graph').removeClass('col-md-9');
          $('.right_info').removeClass('col-md-3');
          //右边信息显示的样式
          $('.right_info').css({
            'display':'none',
            'height': ''
          });
          //节点旁边输入框显示为none
          $('#edit').css('display','none');
          $("#edit input").removeAttr('autofocus','autofocus')
          //详情按钮不显示
          $('.detailEdit').css('display','none');
          $('.detailEditModal').css('display','none');
          //编辑按钮不显示。。。可删除
          $('#edit_btn').css('display','none');
        }
        selected = selected_node;//全局的节点
//          showInfo();
      }

    }
  }



</script>

<style scoped>
  .edit{
    padding-left:10px;
    /*border-radius: 4px;	   */
    background: rgba(225,225,225,0.5);
    box-shadow: 0px 0px 5px lightgray;

  }
  #edit{
    display: none;
    position: absolute;
    z-index: 99;
    border-bottom: 3px solid rgb(113,118,244);
    /*opacity: 0.3;*/
  }
  #edit0{
    /*float: right;*/
    width: 370px;
    margin: auto;
  }
  .words{
    /*width:300px;*/
    margin: 0;
    box-sizing: border-box;
    border: none;
    outline: none;
    background: none;
  }
  .submit{
    margin: 0;
    box-sizing: none;
    border: none;
    background: none;
    outline: none;
  }
  .btn-self{
    display: none;
    float:right;
    padding:0;
    margin-left: 10px;
  }
  svg {
    background-color: #FFF;
    cursor: default;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    -o-user-select: none;
    user-select: none;
  }

  svg:not(.active):not(.ctrl) {
    cursor: crosshair;
  }
svg g .link{
  stroke:lavender;
  stroke-width: 2px;
  cursor: default;
}
  path.link,path.text {
    fill: none;
    /*stroke: rgb(113,118,244);*/
    stroke:lavender;
    stroke-width: 2px;
    cursor: default;
  }

  svg:not(.active):not(.ctrl) path.link {
    cursor: pointer;
  }
  svg:not(.active):not(.ctrl) path.text {
    cursor: pointer;
  }
  .id{
    cursor: pointer;
  }
  path.link.selected {
    stroke-dasharray: 10,2;
  }

  path.link.dragline {
    pointer-events: none;
  }

  path.link.hidden {
    stroke-width: 0;
  }

  circle{
    fill: rgb(136,228,179);
  }
  circle.node {
    /*stroke-width: 1.5px;*/

    cursor: pointer;
  }

  circle.node.reflexive {
    stroke: rgb(90,82,159) !important;
    stroke-width: 2.5px;
  }

  text {
    font: 12px sans-serif;
    pointer-events: none;
  }

  text.id {
    text-anchor: middle;
    font-size:15px;
    color: darkgray;
    /*font-weight: bold;*/
  }
</style>
