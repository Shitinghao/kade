<template>
  <div>
    <!--entity detail-->
    <el-drawer title="实体详情"
               :visible.sync="table"
               direction="rtl"
               size="50%" style="overflow:scroll">
      <el-table :data="gridData">
        <el-table-column property="o" label="O" width="150"></el-table-column>
        <el-table-column property="p" label="P" width="200"></el-table-column>
        <el-table-column property="s" label="S"></el-table-column>
      </el-table>
    </el-drawer>
    <!--node button group-->

    <el-row>
      <div id="button_group" style="box-shadow:0 0 2px lightgrey;position: absolute;background:rgba(225,225,225,0.6);z-index:2;padding:0 10px;display: none;width: 140px;">
        <el-tooltip content=" 隐藏节与关系" placement="bottom" effect="light">
          <el-button type="info" size="mini" circle icon="el-icon-minus"  class="node_hide circle" @click="hide_option"></el-button>
        </el-tooltip>
        <el-tooltip content="功能扩展" placement="bottom" effect="light">
          <el-button type="primary" size="mini" circle icon="el-icon-magic-stick" class="edit_word circle" ></el-button>
        </el-tooltip>
        <el-tooltip content="删除节点" placement="bottom" effect="light">
          <el-button type="danger" size="mini" circle icon="el-icon-close" class="delete circle" @click="remove_option"></el-button>
        </el-tooltip>
      </div>
    </el-row>

    <el-row class="right hideSingle">
      <el-tooltip content="隐藏孤立点" placement="bottom" effect="light">
        <el-button type="info" size="mini" circle icon="el-icon-zoom-out" class="delete circle" @click="hideSingle_option"></el-button>
      </el-tooltip>
      <!--<el-tooltip content="筛选关系" placement="bottom" effect="light">-->
        <!--<el-button type="info" size="mini" circle icon="el-icon-document-checked" class="delete circle" @click="select_option"></el-button>-->
        <!--<el-button type="info" size="mini" circle icon="el-icon-document-checked" class="delete circle" @click="select_option"></el-button>-->
        <el-select v-model="value" clearable placeholder="请选择">
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value">
          </el-option>
        </el-select>
      <!--</el-tooltip>-->
    </el-row>
    <!-- link edit input -->
    <div id="edit" class="edit">
      <input type="text" name="" id="words" class="words" autofocus="autofocus" value="" />
    </div>
    <!--node search component-->
    <div style="box-shadow: 0 0 5px lightgrey;position: absolute;left:10px;top:100px; padding: 10px;z-index: 99;border-radius: 5px; visibility:hidden;">
      <div class="dropdown">
        <button type="button" class="btn dropdown-toggle" id="dropdownMenu1" data-toggle="dropdown">
          组件
          <span class="caret"></span>
        </button>
        <ul class="dropdown-menu" role="menu" aria-labelledby="dropdownMenu1">
          <li role="presentation" class="dropdown-header">检索实体</li>
          <li role="presentation">
            <form action="" role="form" id="Search" style="margin: 10px">
              <div class="form-group">
                <input type="text" class="form-control input-sm" placeholder="请输入节点信息">
              </div>
            </form>
          </li>
          <li role="presentation" class="divider"></li>
          <li role="presentation">
            <a role="menuitem" tabindex="-1" href="#" @click="table = true">实体详情</a>
          </li>
        </ul>
      </div>
    </div>
    <!-- show node svg -->
    <div class="left_graph col-xs-12"></div>
    <!--  delete node/link warning-->
    <el-dialog title="删除实体" :visible.sync="entDelDialogVisible" width="50%">
      <span>将要删除实体 {{ent_dels.eid}} , 以下关系也将被同步删除：</span>
      <el-table :data="delEntData" style="width: 100%" center="True">
        <el-table-column prop="s" label="Subject"></el-table-column>
        <el-table-column prop="p" label="Preidcate"></el-table-column>
        <el-table-column prop="o" label="Object"></el-table-column>
      </el-table>
      <span slot="footer" class="dialog-footer">
        <el-button @click="entDelDialogVisible=false">取 消</el-button>
        <el-button type="primary" @click="remove_entity(ent_dels.eid)">确 定</el-button>
      </span>
    </el-dialog>
    <!--show entity-->
    <el-dialog title="显示实体" :visible.sync="showEntDialogVisible" width="40%" :before-close="handleClose">
      <el-row class="demo-autocomplete">
        <el-col :span="24">
          <el-autocomplete v-model="ent_select.eid"
                           :fetch-suggestions="objectSuggestion"
                           style="width:100%"
                           placeholder="请输入需要显示实体的名称"></el-autocomplete>
        </el-col>
      </el-row>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showEntDialogVisible=false">取 消</el-button>
        <el-button type="primary" @click="showEntity()">确 定</el-button>
      </span>
    </el-dialog>
    <!-- add link -->
    <el-dialog title="新增关系" :visible.sync="dialogVisible" width="50%" :before-close="handleClose">
      <div class="input_style">
        <label for="" style="float: left;">Subject: </label>
        <el-input type="text" v-model="inserts.sid" placeholder="" :disabled="true"></el-input>
      </div>
      <div class="input_style">
        <label for="" style="float: left;"> Predicate:</label>
        <el-input type="text" v-model="inserts.p" placeholder=""></el-input>
      </div>
      <div class="input_style">
        <label for="" style="float: left;"> Object:</label>
        <el-input type="text" v-model="inserts.oid" placeholder="" :disabled="true"></el-input>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible=false">取 消</el-button>
        <el-button type="primary" @click="submitNewTriple">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
  import * as d3 from 'd3'
  import global from './nav.vue'
  export default {
    name: "nodeGraph",
    data() {
      return {
        api_host: global.api_host,
        table: false,
        dialog: false,
        loading: false,
        gridData: global.entityInfo,
        ent_dels: {eid: ""},
        delEntData: [],
        entDelDialogVisible: false,
        showEntDialogVisible: false,
        dialogVisible: false,
        ent_select: { ename:"", eid: "", options:[]},
        ent_inserts: { ename: '' },
        inserts: { sid: '', p: '', oid: '', oname: '', old_tid: '' },
        searchWords: global.main_entity,
        selectedNode:'12312',
        options:[{
          value: '选项1',
          label: '黄金糕'
        }, {
          value: '选项2',
          label: '双皮奶'
        }, {
          value: '选项3',
          label: '蚵仔煎'
        }, {
          value: '选项4',
          label: '龙须面'
        }, {
          value: '选项5',
          label: '北京烤鸭'
        }],
        value: ''
      };

    },
    methods: {
      make_readable_id(name, id) {
        if (name === id) return id;
        return name + "<id:" + id + ">";
      },
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
      submitNewEntity(callback) {
        let _this = this;
        this.checkAndSubmit(this, this.api_host+'/api/new_entity', {
              name: this.ent_inserts.ename
          },
          function (response, _this) {
            let ename = _this.ent_inserts.ename;
            _this.ent_inserts.ename = "";
            _this.svg.classed('active', true);
            callback(response);
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
            let options = [];
            ents.forEach(function (x) {
              options.push({
                link: x.ename,
                value: _this.make_readable_id(x.ename, x.eid)
              });
            });
            cb(options);
          })
          .catch(function (error) {
            console.log(error);
          });
      },
      findNode(idx) {
        let xx = this.nodes.filter(x => (x.idx === idx));
        return xx[0];
      },
      checkRepNodes(node) {
        let xx = this.nodes.filter(x => (x.idx === node.idx));
        return xx.length == 0;
      },
      checkRepLinks(link) {
        let xx = this.links.filter(x => (x.triple.idx === link.triple.idx));
        return xx.length == 0;
      },
      showEntity(eeid, do_expand) {
        let _this = this;
        let point = null;
        let exid = eeid;

        if (eeid == null) {
          point = _this.ent_select.point;
          exid = _this.ent_select.eid;
        }

        if (_this.nodes.length == 0) do_expand = 1;

        let no_expand = 1;
        if (do_expand != null) no_expand = "";

        this.axios
          .get(_this.api_host+"/api/graph/query_entity", {
            params: {
              idx: exid,
              no_expand: no_expand
            }
          })
          .then(function (response) {
            if (response.data.nodes.length === 0) {
              _this.ent_inserts.ename = exid;
              _this.$confirm('是否新建名为 ' + exid + ' 的实体？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'info'
              }).then(() => {
                _this.submitNewEntity(function (response) {
                  let node = {
                    id: ++_this.lastNodeId, idx: response.data.eid,
                    name: exid, reflexive: false, info: []
                  };
                  if (point != null) {
                    node.x = point[0];
                    node.y = point[1];
                  }
                  _this.nodes.push(node);
                  _this.showEntDialogVisible = false;
                  _this.restart();
                });
              }).catch(() => {   
              });
              return;
            }
            $.each(response.data.nodes, function(i,val) {
              let node = { id: ++_this.lastNodeId, idx: val.idx, name: val.idx, reflexive: false, info: val.attr };
              if (val.name != null)  node.name = val.name;
              if (point != null) {
                 node.x = point[0];
                 node.y = point[1];
              }
              if (_this.checkRepNodes(node)) _this.nodes.push(node);
            });
            $.each(response.data.links, function (i, val) {
              let snode = _this.findNode(response.data.nodes[val.source].idx);
              let onode = _this.findNode(response.data.nodes[val.target].idx);
              let link = {source: snode, target: onode,
                left: false, right: true, relation: val.triple.p,
                triple: val.triple
              }
              if (_this.checkRepLinks(link)) _this.links.push(link);
            });

            _this.showEntDialogVisible = false;
            _this.restart();
          })
          .catch(function (error) {
            // console.log(error);
          });
      },
      submitNewTriple() {
        let _this = this;
        this.checkAndSubmit(this, this.api_host+'/api/new_triple', {
            sid: this.inserts.sid,
            p: this.inserts.p,
            oid: this.inserts.oid,
            oname: this.inserts.oid,
            old_tid: this.inserts.old_tid
          },
          function (response, _this) {
            //if (_this.inserts.old_tid !== "") {
            //  _this.remove_triple(_this.inserts.old_tid);
            //  _this.inserts.old_tid = "";
            //}
            console.log(response);
            _this.inserts.link.triple.idx = response.data.eid;
            _this.inserts.link.relation = _this.inserts.p;
            _this.inserts.link.triple.p = _this.inserts.p;
            _this.links.push(_this.inserts.link);
            _this.inserts = { sid: '', p: '', oid: '', old_tid: '' };
            _this.dialogVisible = false;
            _this.restart();
          },
          function (response, _this) {
            _this.$message.error(response.data.msg);
          }
        );
      },
      show_help() {
        const h = this.$createElement;

        this.$notify({
          title: '使用提示',
          message: h('i', { style: 'color: teal' },
            '双击空白部分以选择要显示的节点，点击元素以进行更改，在实体间连线以新增关系, 按CTRL键拖动节点。选定节点按Enter以扩展节点。')
        });
      },

      remove_entity(tid) {
        let _this = this;
        this.axios
          .get(this.api_host+'/api/remove_entity', {
            params: {
              id: tid
            }
          })
          .then(function (response) {
            _this.nodes.splice(_this.nodes.indexOf(_this.ent_dels.related_node), 1);
            _this.spliceLinksForNode(_this.ent_dels.related_node);
            $('.tooltip').css('display','none');
            _this.entDelDialogVisible = false;
            _this.ent_dels.eid = "";
            _this.restart();
          })
          .catch(function (error) {
            console.log(error);
          });
      },
      remove_option(){
        let _this = this;
        _this.deleteNode(_this.selectedNode,true);
      },
      hide_option(){
        let _this = this;
        _this.deleteNode(_this.selectedNode,false);
      },
      hideSingle_option(){
        let _this = this;
        _this.hideSingle(_this.selectedNode,true);

      },
      select_option(){
        console.log('select');
      },
      showRemoveEntDialog(eid) {
        let _this = this;
        this.ent_dels.eid = eid;
        this.axios
          .get(this.api_host+'/api/info_remove_entity', {
            params: {
              id: eid
            }
          })
          .then(function (response) {
            _this.delEntData = response.data.ret;
            _this.entDelDialogVisible = true;
          })
          .catch(function (error) {
            console.log(error);
          });
      },
    },
    mounted() {
      var _this = this;
      var width = $('.left_graph').width(),
      height = window.innerHeight-79 ,
      colors = d3.scale.category10();

      _this.show_help();

      var svg = d3.select('.left_graph')
        .append('svg')
        .attr('class','layout')
        .attr('width', width)
        .attr('height', height);

      var nodes = [];
      var links = [];
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
      var entitydelete = false;
      var select_Entity = null;
      var select_line = null;
      var removeLine = [];

      _this.nodes = nodes;
      _this.links = links;
      _this.svg = svg;
      _this.lastNodeId = null;
      _this.removeLine = removeLine;

      


      // mouse event vars
      var selected_node = null,
        selected_link = null,
        selected_link_text = null,
        mousedown_link = null,
        mousedown_link_text = null,
        mousedown_node = null,
        mouseup_node = null;

       _this.selected_node = selected_node;


      var tooltip = d3.select("body")
        .append("div")//添加div并设置成透明
        .attr("class","tooltip")
        .style("opacity", 0.0);

      var path, path_text, circle, drag_line;
      
      function restart() {
        let force = _this.force;
        if (!force) return;

        $("svg").empty();
      // line displayed when dragging new nodes
      drag_line = svg.append('svg:path')
        .attr('class', 'link dragline hidden')
        .attr('d', 'M0,0L0,0');

      // handles to link and node element groups
      path = svg.append('svg:g').selectAll('path'),
      path_text = svg.append("g").selectAll(".edgelabel"),
      circle = svg.append('svg:g').selectAll('g');

      
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
          'dx':30,
          'dy':0
        });

        // add new path text
        path_text.enter().append("text")
          .attr({
            'class':'edgelabel',
            'id':function(d,i){return 'edgepath'+ i;},
            'dx':30,
            'dy':0
          })
          .append('textPath')
          .attr('xlink:href',function(d,i) {return '#edgepath'+i})
          .style("pointer-events", "auto")
          .attr('class','ptext')
          .text(function(d){return d.relation;})
          .on('mouseover',function (d) {
            d3.select(this).style('cursor', 'pointer');
          })
          .on('mousedown',function(d){
            if(d3.event.ctrlKey) return;
            //设置样式与数据
            mousedown_link_text = d;

            selected = mousedown_link_text;
            $("#edit").css('display','block');
            $('.detailEdit').css('display','none');
            $("#words").val(d.relation);
            $("#words").removeAttr("disabled");

            edit_relation = true;
            svg.selectAll('.ptext')
              .style('fill','black')

            if (mousedown_link_text === selected_link_text) selected_link_text = null;
            else {
              selected_link_text = mousedown_link_text;
              selected_link = mousedown_link_text;
            }
            console.log(selected_link_text);
            if(selected_link_text == null){
              d3.select(this).style('fill','black');
              $("#edit").css({
                'display':'none',
              });
            }else{
              d3.select(this).style('fill','#1E90FF');
              $("#edit").css({
                'display':'inline-block',
                "top":(d.target.y - d.source.y)/2 + d.source.y + 70 + "px",
                "left":(d.target.x - d.source.x)/2 + d.source.x + "px",
              });
              selected_node = null;
              if (selected_node == null){
                $("#button_group").css('display','none');
              }

            }


            //输入框聚焦
            $("#words").focus();
            restart();
          })
          .on('mouseup',function (d) {
            //输入框聚焦
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
          // .attr('r', 12)
          .attr('r', function(d){
            // console.log(d.name );
            // console.log(nodes[0].name);
            if (d.name == nodes[0].name){
              return 15;
            }else{
              return 10;
            }
          })
          .style('fill', function(d) {
            return (d === selected_node) ? d3.rgb(150,215,250).brighter().toString() : d3.rgb(150,215,250);
          })
          .classed('reflexive', function(d) { return d.reflexive; })
          .on('mouseover', function(d) {
            d3.select(this).style('cursor', 'pointer');
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
            if (mousedown_node === selected_node) selected_node = null;
            else {
              selected_node = mousedown_node;
              global.main_entity = _this.make_readable_id(selected_node.name, selected_node.idx);
              global.entityInfo = selected_node.info;
            }

            //显示info信息

            // aboutInfo(selected_node);
            //选中节点后，调用SELECT（）计算4个象限
            //findnode
            if(selected_node == null ){
              //newResult = findNode(selected_node);
              //i = 0;
              console.log('no seleeted');
              $("#button_group").css({'display':'none'});
            }else{
              $("#button_group").css({
                'display':'inline-block',
                "top":selected_node.y-20+70 + "px",
                "left":selected_node.x+30 + "px",
              });
              selected_link = null;
              selected_link_text = null;
              _this.selectedNode = selected_node;
              if (selected_link_text == null){
                $("#edit").css('display','none');
                svg.selectAll('.ptext')
                  .style('fill','black')

              }

              //关于space的节点遍历
              newResult = findNode(selected_node);
              // SELECT(selected_node);
              i = 0;
            }

            // reposition drag line
            drag_line
              .style('marker-end', 'url(#end-arrow)')
              .style({
                'stroke':'lavender',
                'stroke-width': '2px',
                ' cursor': 'default'
              })
              .classed('hidden', false)
              .attr('d', 'M' + mousedown_node.x + ',' + mousedown_node.y + 'L' + mousedown_node.x + ',' + mousedown_node.y);
            restart();
          })
          .on('mouseup', function(d) {  // 拖动新增关系
            if(!mousedown_node) return;
            //因为在mousedown事件比up事件靠前，所以，将focus事件写在mousedown里面不生效（不会执行），mousedown > focus > mouseup > click
            $("#edit input").focus();
            // needed by FF
            drag_line
              .classed('hidden', true)
              .style('marker-end', '')
              .style({
                'stroke':'none',
                'stroke-width': '0px',
                ' cursor': 'pointer'
              })
              ;

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

            console.log(source);
            console.log(target);
            _this.inserts.sid = mousedown_node.idx;
            if (mousedown_node.name !== mousedown_node.idx)
              _this.inserts.sid = _this.make_readable_id(mousedown_node.name, mousedown_node.idx)
            _this.inserts.p = "";
            _this.inserts.oid = mouseup_node.idx;
            if (mouseup_node.name !== mouseup_node.idx)
              _this.inserts.oid = _this.make_readable_id(mouseup_node.name, mouseup_node.idx)
            _this.dialogVisible = true;
            //修改了source与target的数据，原因是source指出去的，target是指向的点，按原本的操作变反了
            link = {
              source:source , target: target, left: false, right: false,
              relation: '', triple: { idx: '', o: _this.inserts.oid, p: '', s: _this.inserts.sid }
            }
            link[direction] = true;
            console.log(links);
            _this.inserts.link = link;
          });

        // show node IDs
        g.append('svg:text')
          .attr('x',function (d) {
            if(d.name == nodes[0].name){
              return -30
            }else {
              return -16;
            }

            })
          // .attr('y', 4)//-16
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
            },
            'font-weight':function (d) {
              if (d.name == nodes[0].name){
                return '500'
              }

            }
          })
          .text(function(d) {
            if(d.name.length>10){
              d.name = d.name.substr(0,10)+'...';
              return  d.name;
            }else{
              return  d.name;
            }
          });

        // remove old nodes
        circle.exit().remove();
        // set the graph in motion
        force.start();
      } // function restart end

      _this.restart = restart;

      start();
      function start() {
        var force = d3.layout.force()
            .nodes(nodes)
            .links(links)
            .size([width, height])
            .linkDistance(150)
            .charge(-500)
            .on('tick', tick);

        _this.force = force;

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

        if (_this.searchWords !== "") {
          _this.showEntity(_this.searchWords, true);
        }
        // function start  end
      }

      _this.start = start;

      function spliceLinksForNode(node) {
        var toSplice = links.filter(function(l) {
          return (l.source === node || l.target === node);
        });
         _this.removeLine = toSplice;

        toSplice.map(function(l) {
          links.splice(links.indexOf(l), 1);
        });
      }
      _this.spliceLinksForNode = spliceLinksForNode;

      function resetMouseVars() {
        mousedown_node = null;
        mouseup_node = null;
        mousedown_link = null;
        mousedown_link_text = null;
      }

      function mousedown() {
        // prevent I-bar on drag
        //d3.event.preventDefault();
        if (d3.event.ctrlKey || mousedown_node || mousedown_link || mousedown_link_text) return;
        var point = d3.mouse(this), timest = new Date().getTime();
        _this.ent_select.point = point;
        _this.ent_select.timest = timest;
        _this.ent_select.eid = "";
        _this.showEntDialogVisible = true;
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

      // only respond once per keydown
      var lastKeyDown = -1;
      var i= 0;
      var newResult = null;

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

      function keydown() {
        //d3.event.preventDefault();//阻止了所有的默认的键盘事件
        let force = _this.force;
        if (!force) return;

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
            deleteNode(selected_node,true);
            break;
          case 13: // enter
            _this.showEntity(selected_node.idx, true);
            break;
          case 37://left
            if(selected_node){
              if (SELECT(selected_node).left == undefined){
                return false;
              }else{
                selected_node = SELECT(selected_node).left.data.data;
                // aboutInfo(selected_node);
                $("#button_group").css({
                  'display':'inline-block',
                  "top":selected_node.y-20+70 + "px",
                  "left":selected_node.x+30 + "px",
                });
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
                // aboutInfo(selected_node)
                $("#button_group").css({
                  'display':'inline-block',
                  "top":selected_node.y-20+70 + "px",
                  "left":selected_node.x+30 + "px",
                });
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
                // aboutInfo(selected_node);
                $("#button_group").css({
                  'display':'inline-block',
                  "top":selected_node.y-20+70 + "px",
                  "left":selected_node.x+30 + "px",
                });
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
                // aboutInfo(selected_node);
                $("#button_group").css({
                  'display':'inline-block',
                  "top":selected_node.y-20+70 + "px",
                  "left":selected_node.x+30 + "px",
                });
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
            if(selected_node){
              $("#edit").css({'display':'none',});
              $("#button_group").css({'display':'none'})
            }
            if(selected_link_text){
              $("#edit").css({'display':'none',});
            }
            restart();
            break;
          case 72://hide
            deleteNode(selected_node,false);
            break;
        }
      }

      svg.on('dblclick', mousedown)
        .on('mousemove', mousemove)
        .on('mouseup', mouseup);
      d3.select(window)
        .on('keydown', keydown)
        .on('keyup', keyup);


      svg.style('width','100%');

      //delete
      function deleteNode(selected_node,isdelete){
        if(isdelete) { //isselect来判断是隐藏还是删除，true是删除，false是隐藏
          if (selected_node) {
            let should_remove_eid = selected_node.idx;
            _this.ent_dels.related_node = selected_node;
            _this.showRemoveEntDialog(should_remove_eid);
          } else if (selected_link) {
            let should_remove_link = selected_link;
            _this.$confirm('确定要删除关系吗？')
              .then(_ => {
                _this.axios
                  .get(_this.api_host + '/api/remove_triple', {
                    params: {
                      id: should_remove_link.triple.idx,
                    }
                  })
                  .then(function (response) {
                    console.log(should_remove_link);
                    console.log(_this.links);
                    _this.links.splice(_this.links.indexOf(should_remove_link), 1);
                    console.log(_this.links);
                    _this.restart();
                  })
                  .catch(function (error) {
                    console.log(error);
                  });
              })
              .catch(_ => {
              });
          }
        }else{
          if (selected_node) {
            _this.nodes.splice(_this.nodes.indexOf(selected_node),1);
            spliceLinksForNode(selected_node);
            console.log();
            console.log(_this.removeLine);
            var tNode = [];
            $.each(_this.removeLine,function(i,val){
              tNode.push(val.target);
              tNode.push(val.source);
            })
            var tNode = [...new Set(tNode)];
            tNode.splice(tNode.indexOf(selected_node),1);
            // console.log(tNode);
            

            // hideSingle(tNode,false);
          } else if (selected_link) {
            let should_remove_link = selected_link;
            _this.links.splice(_this.links.indexOf(should_remove_link), 1);
          }
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
        $("#button_group").css('display','none');
        tooltip.style("opacity",0.0);
        tooltip.style('display','none');
      }
      _this.deleteNode = deleteNode;

      //hide single node
      function hideSingle(tNode,clickHide){
        var linkTargetNodesArr = [];
        var linkSourceNodeArr = [];
        $.each(links,function(i,val){
            linkTargetNodesArr.push(val.target);
            linkSourceNodeArr.push(val.source);
        })
        var newNode =linkSourceNodeArr.concat(linkTargetNodesArr);
            newNode = [...new Set(newNode)];
        var myArray = [];//要删除的孤立点
        if (newNode.length != nodes.length && nodes.length> newNode.length){
            myArray = $.grep(nodes,function (value){
              return $.inArray(value,newNode) < 0;
          })
        }
        console.log(myArray);
        // //第二遍
        console.log(clickHide);
        if(clickHide == true){  //如果点击单个清除单个节点的按钮，就清除页面中的所有的孤立点
          $.each(myArray,function(i,val){
            nodes.splice(nodes.indexOf(val),1);
            --_this.lastNodeId;
          });
        }else{    //selected_node中的hide操作
          console.log(tNode); //selecte节点的相关节点
          console.log(myArray);//放置孤立点的数组
          var nolinkNode = myArray.filter(function (el) { //在myArray中删除包含的tNode中包含的所有元素
            return tNode.indexOf(el) < 0 ;
          })
          console.log(nolinkNode);//新增的孤立的节点
          if(myArray.length>nolinkNode.length){ //孤立节点数组的长度 > 新增的孤立节点数 也就是说绝对为true（因为nolinkNode就是myArray的元素）
            myArray = myArray.filter(function (el) {
              return nolinkNode.indexOf(el) < 0 ;
            })
          }
          // myArray = myArray.filter(function (el) {
          //   return nolinkNode.indexOf(el) < 0 ;
          // })
          console.log(myArray); //拿到的是selected_node的相关关系的孤立点

          //判断如果在myArray中没有tnode
          var containIndex = true;
          if (tNode.length > myArray.length){
            $.each(tNode,function(i,val){
              if (myArray.includes(val)){
                containIndex = true;
              } else{
                containIndex = false;
              }
            })
          }else{
            $.each(myArray,function(i,val){
              if (tNode.includes(val)){
                console.log('yes');
                containIndex = true;
              } else{
                console.log('no');
                containIndex = false;
              }
            })
          }

          if (containIndex == true){
            $.each(myArray,function(i,val){
              nodes.splice(nodes.indexOf(val),1);
              --_this.lastNodeId;
            });
          }
        }

        //初始化操作，将选中的节点或者连线选中状态取消
        selected_link = null;
        selected_node = null;
        restart();
        $.each(nodes,function(i,val){
          val.id = i;
        });
        $("#edit").css('display','none');
        $("#button_group").css('display','none');
        tooltip.style("opacity",0.0);
        tooltip.style('display','none');

      }
      _this.hideSingle = hideSingle;



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
        right = nodeDistance(selected_node , rightArray);
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
      $('#Search').on('submit', function () {
        _this.searchWords = $('#Search .form-control').val();
        global.main_entity = _this.searchWords;
        selected_node = null;

        svg.selectAll().remove();

        console.log(_this.searchWords);
        _this.nodes.length = 0;
        _this.links.length = 0;
        restart();

        _this.lastNodeId = null;
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
          //$.post('http://47.101.181.52:22222/api/cndbpedia/graph/update_entity',{'idx':selected.idx,'new_id':selected.name},function(result){
          //
          //  result = JSON.parse(result);
          //  console.log(result);
          //});
          //判断是否是便捷节点的状态

          if(edit_relation==true){
            //选择所有的连线文字，重新绘制文字，并恢复修改后为黑色字体
            svg.selectAll('.ptext')
              .style('fill','black')
              .text(function(selected){return selected.relation});
            //发送数据请求
            console.log(selected_link_text);
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
            "top":selected_node.y+10 + "px",
            "left":selected_node.x+ "px",
          });
          // $('#edit input').css('display','block');

          //详情按钮显示
          $('.detailEdit').css('display','block');
          $('.detailEditModal').css('display','block');
          //编辑按钮显示。。。可以删除
          $('#edit_btn').css('display','block');
          //节点跟前的输入框中val赋值

          $("#words").attr("disabled", "disabled");
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
    padding:0 10px;
    /*border-radius: 4px;	   */
    background: rgba(225,225,225,0.5);
    box-shadow: 0px 0px 5px lightgray;
    /*width: 150px;*/
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
  .el-drawer__body{
    overflow: scroll;
  }
  .hideSingle{
    border: 1px solid #b4bccc;
    padding: 10px;margin: 10px;
    /*position: fixed;*/
    /*right: 0;*/
  }

</style>
