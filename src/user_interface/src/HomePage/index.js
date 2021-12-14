import React, { useEffect, useState} from 'react';
import axios from 'axios'
import ReactDOM from 'react-dom';
import '../index.css';
import cloneDeep from 'lodash.clonedeep';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  useHistory,
  useLocation,
  useParams
} from "react-router-dom";
import ReactECharts from 'echarts-for-react';  // or var ReactECharts = require('echarts-for-react');


axios.defaults.baseURL='http://127.0.0.1:5000';

global.var= {
 threshold:0,
 lumin:100,
 blind:"Under control"
};


class DCI extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        cur_light:0

  }
}
  componentDidMount() {
    this.timerID = setInterval(
      () => this.tick(),
      5000
    );
  }
  componentWillUnmount() {
    clearInterval(this.timerID);
  }

  tick() {
    let Data={"type":2,"threshold":0,"lumin":global.var.lumin}
    fetch('/Home',{
      method:'post',
      headers:{
          'Accept':'application/json,text/plain,*/*',/* 格式限制：json、文本、其他格式 */
          'Content-Type':'application/x-www-form-urlencoded'/* 请求内容类型 */
      },
      body:JSON.stringify(Data)
  }).then((response)=>{
      return response.json()
  }).then((data)=>{
    this.setState ({
      cur_light: data["ifchange"]
     });
    console.log(this.state.ifchange)
  }).catch(function(error){
      console.log(error)
  })
  global.var.lumin=this.state.cur_light
  }
  render() {
    return (
      <div className="count">
       
        <h1>Current Light Intensity: {this.state.cur_light}</h1>
        <h1>Current Blind: {global.var.blind}</h1>
      </div>
    );
  }
}




class Set_Part extends React.Component{
  constructor(props) {
    super(props);
    this.state={
      threshold:'',
      value1: '',
      ifchange:'',
      enter_handle:false,
      open_time:'',
      close_time:'',
      value2:'',
      value3:'',
      type:0

    }
    
    this.set_threshold=this.set_threshold.bind(this);
    this.set_opentime=this.set_opentime.bind(this);
    this.set_closetime=this.set_closetime.bind(this);
  }
  componentDidMount() {
    // 默认值
    this.setState({
      value1: this.props.value1 || ''
    })
  }
  ChangeHandle1(e) {
    // 监控变化
    this.setState({
      value1: e.target.value
    })
  }
  KeyUpHandle1(e) {
    // 监控 enter 事件
    if (e.keyCode !== 13) {
      return
    }
    // 加验证
    if (e.target.value) {
      this.setState({
        enter_handle:true
      })
    }else {
      alert('')
    }
  }

  set_threshold(){
    //set threshold here
    this.state.threshold=this.state.value1
    global.var.threshold=this.state.threshold
    let Data={"type":1,"threshold":this.state.threshold,"lumin":global.var.lumin}
    fetch('/Home',{
      method:'post',
      headers:{
          'Accept':'application/json,text/plain,*/*',/* 格式限制：json、文本、其他格式 */
          'Content-Type':'application/x-www-form-urlencoded'/* 请求内容类型 */
      },
      body:JSON.stringify(Data)
  }).then((response)=>{
      return response.json()
  }).then((data)=>{
    this.setState ({
      ifchange: data["ifchange"]
     });
    console.log(this.state.ifchange)
  }).catch(function(error){
      console.log(error)
  })
  }
  componentDidMount() {
    // 默认值
    this.setState({
      value2: this.props.value2 || ''
    })
  }
  ChangeHandle2(e) {
    // 监控变化
    this.setState({
      value2: e.target.value
    })
  }
  KeyUpHandle2(e) {
    // 监控 enter 事件
    if (e.keyCode !== 13) {
      return
    }
    // 加验证
    if (e.target.value) {
      this.setState({
        enter_handle:true
      })
    }else {
      alert('')
    }
  }

  set_opentime(){
    //set threshold here
    this.state.open_time=this.state.value2
    global.var.blind="Open"
    let Data={"type":-1,'opentime':this.state.open_time,"lumin":global.var.lumin}
    fetch('/Home',{
      method:'post',
      headers:{
          'Accept':'application/json,text/plain,*/*',/* 格式限制：json、文本、其他格式 */
          'Content-Type':'application/x-www-form-urlencoded'/* 请求内容类型 */
      },
      body:JSON.stringify(Data)
  }).then((response)=>{
      return response.json()
  }).then((data)=>{
    this.setState ({
      ifchange: data["ifchange"]
     });
    console.log(this.state.ifchange)
  }).catch(function(error){
      console.log(error)
  })
  }

  componentDidMount() {
    // 默认值
    this.setState({
      value3: this.props.value3 || ''
    })
  }
  ChangeHandle3(e) {
    // 监控变化
    this.setState({
      value3: e.target.value
    })
  }
  KeyUpHandle3(e) {
    // 监控 enter 事件
    if (e.keyCode !== 13) {
      return
    }
    // 加验证
    if (e.target.value) {
      this.setState({
        enter_handle:true
      })
    }else {
      alert('')
    }
  }

  set_closetime(){
    //set threshold here
    this.state.close_time=this.state.value3
    global.var.blind="Close"
    let Data={"type":-2,'closetime':this.state.close_time,"lumin":global.var.lumin}
    fetch('/Home',{
      method:'post',
      headers:{
          'Accept':'application/json,text/plain,*/*',/* 格式限制：json、文本、其他格式 */
          'Content-Type':'application/x-www-form-urlencoded'/* 请求内容类型 */
      },
      body:JSON.stringify(Data)
  }).then((response)=>{
      return response.json()
  }).then((data)=>{
    this.setState ({
      ifchange: data["ifchange"]
     });
    console.log(this.state.ifchange)
  }).catch(function(error){
      console.log(error)
  })
  }
  render(){
    return (

      <div>
        <br/><br/><br/>
        <input
        className="search-input"
        type="text"
        placeholder="Please Enter Light Intensity Threshold"
        onChange={this.ChangeHandle1.bind(this)}
        onKeyUp={this.KeyUpHandle1.bind(this)}
        value={this.state.value1}/>
        
        <button onClick={this.set_threshold.bind(this)} class="button-1">  set </button>
       
        
        <div>
        <h2>{}</h2>
        </div>

        <div>
        <input
        className="search-input"
        type="text"
        placeholder="Please Enter Time to open the Blind Ex:21:00:00"
        onChange={this.ChangeHandle2.bind(this)}
        onKeyUp={this.KeyUpHandle2.bind(this)}
        value={this.state.value2}/>

         <button onClick={this.set_opentime.bind(this)} class="button-1"> set </button>
        </div>
        <div>
        <h2> </h2>
        </div>
        <div>
        <input
        className="search-input"
        type="text"
        placeholder="Please Enter Time close the Blind Ex:21:00:00"
        onChange={this.ChangeHandle3.bind(this)}
        onKeyUp={this.KeyUpHandle3.bind(this)}
        value={this.state.value3}/>

         <button onClick={this.set_closetime.bind(this)} class="button-1"> set </button>
        </div>

      </div>
    )
  }
}

function Dynamic_Panel(props) {
  if (!props.warn) {
    let Data={"type":1,'threshold':-1,"lumin":global.var.lumin}
    fetch('/Home',{
      method:'post',
      headers:{
          'Accept':'application/json,text/plain,*/*',/* 格式限制：json、文本、其他格式 */
          'Content-Type':'application/x-www-form-urlencoded'/* 请求内容类型 */
      },
      body:JSON.stringify(Data)
  }).then((response)=>{
      return response.json()
  }).catch(function(error){
      console.log(error)
  })
    return null;
  }
  return (
    <div className="setPart">
    <Set_Part/>
    </div>
  );
}

/*major choose part end*/
class Start extends React.Component{
  constructor(props) {
    super(props);
    this.state = {showtime: false}
    this.handle_Time = this.handle_Time.bind(this);
  }
  handle_Time() {
    this.setState(prevState => ({
      showtime: !prevState.showtime
    }));
  }
  render(){
    return (
      <div className="Time">
      <button onClick={this.handle_Time } class="button-28">
      {this.state.showtime ? 'Disable' : 'Enable'}
    </button>
    < Dynamic_Panel warn={this.state.showtime} />
    </div>
    )

  }
}

const Page = () => {
  const options = {
    grid: { top: 8, right: 8, bottom: 24, left: 36 },
    xAxis: {
      type: 'category',
      data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    },
    yAxis: {
      type: 'value',
    },
    series: [
      {
        data: [820, 932, 901, 934, 1290, 1330, 1320],
        type: 'line',
        smooth: true,
      },
    ],
    tooltip: {
      trigger: 'axis',
    },
  };
  return <ReactECharts option={options} />;
};

const Page2 = () => {
  const DEFAULT_OPTION = {
    title: {
      text:"",
    },
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data:['LIGHT INTENSITY']
    },
    toolbox: {
      show: true,
      feature: {
        dataView: {readOnly: false},
      }
    },
    grid: {
      top: 60,
      left: 30,
      right: 60,
      bottom:30
    },
    dataZoom: {
      show: false,
      start: 0,
      end: 100
    },
    xAxis: [
      {
        type: 'category',
        boundaryGap: true,
        data: (function (){
          let now = new Date();
          let res = [];
          let len = 50;
          while (len--) {
            res.unshift(now.toLocaleTimeString().replace(/^\D*/,''));
            now = new Date(now - 5000);
          }
          return res;
        })()
      }
    ],
    yAxis: [
      {
        type: 'value',
        scale: true,
        name: "Light Intensity",
        max: 1000,
        min: 0,
        boundaryGap: [0.2, 0.2]
      }
    ],
    series: [
      {
        name:'Light Intensity',
        type:'line',
        lineStyle:{ 
          normal:{ color: "#d14a61"  }//线条的颜色及宽度
      },
        data:(function (){
          let res = [];
          let len = 0;
          while (len < 50) {
            res.push(0);
            len++;
          }
          return res;
        })()
        
      },
      {
        name:'Threshold',
        type:'line',
        lineStyle:{ 
          normal:{color: '#5793f3' }//线条的颜色及宽度
      },
        data:(function (){
          let res = [];
          let len = 0;
          while (len < 50) {
            res.push(0);
            len++;
          }
          return res;
        })()
      }
    ]
  };

  let count;

  const [option, setOption] = useState(DEFAULT_OPTION);

  function fetchNewData() {
    const axisData = (new Date()).toLocaleTimeString().replace(/^\D*/,'');
    const newOption = cloneDeep(option); // immutable
    newOption.title.text = "light";
    /* const data0 = newOption.series[0].data; */
    const data1 = newOption.series[0].data;
    const data2=newOption.series[1].data;
    /* data0.shift();
    data0.push(Math.round(Math.random() * 1000)); */
    let Data={"type":3}
    //get data for the line
    fetch('/Home',{
      method:'post',
      headers:{
          'Accept':'application/json,text/plain,*/*',/* 格式限制：json、文本、其他格式 */
          'Content-Type':'application/x-www-form-urlencoded'/* 请求内容类型 */
      },
      body:JSON.stringify(Data)
  }).then((response)=>{
      return response.json()
  }).then((data)=>{
    data1.shift();
    data1.push(data["data"])
    data2.shift();
    data2.push(global.var.threshold)
    console.log(this.state.ifchange)
  }).catch(function(error){
      console.log(error)
  })
    
    ;

    newOption.xAxis[0].data.shift();
    newOption.xAxis[0].data.push(axisData);
   /*  newOption.xAxis[1].data.shift();
    newOption.xAxis[1].data.push(count++); */

    setOption(newOption);
  }

  useEffect(() => {
    const timer = setInterval(() => {
      fetchNewData();
    }, 5000);

    return () => clearInterval(timer);
  });

  return <ReactECharts
    option={option}
    style={{ height: 400 }}
  />;
};



/*包括title 和几个其他组件*/
function Home (){
  const[comment, setComment]=useState(0);
  useEffect(()=>{
    fetch('/Home').then(res=>res.json()).then(data=>{
       setComment(data.time)
    });
},[]);
    return (
      <div>
      <div class="header"><h1>BLIND CONTROLER</h1></div>
      <div class="content">
        <div class="menu"><br/><br/><br/><br/><DCI/><br/><br/><Start/></div>
        <div class="main"> <br/><br/><br/><Page2/></div>
      </div>
      </div>
    );
  }

export default Home;
