import{cV as P,cA as _,eG as T,R as G,B as M,E as m,j as u,a0 as w,a1 as C,ev as D,eH as $}from"./index-CfA4yAo4.js";import{b as B,a as R}from"./DzCrTKgRRq.js";import{u as V,g as k,f as F,a as H,G as x}from"./7BkxPALTV7.js";function U(e,a,t,i){for(var s=-1,o=e==null?0:e.length;++s<o;){var l=e[s];a(i,l,t(l),e)}return i}var W=U,Y=B;function q(e,a,t,i){return Y(e,function(s,o,l){a(i,s,t(s),l)}),i}var z=q,J=W,K=z,L=R,Q=P;function X(e,a){return function(t,i){var s=Q(t)?J:K,o=a?a():{};return s(t,e,L(i),o)}}var N=X,Z=T,ee=N,te=Object.prototype,re=te.hasOwnProperty,ae=ee(function(e,a,t){re.call(e,t)?e[t].push(a):Z(e,t,[a])}),ne=ae;const se=_(ne);var oe=N,ie=oe(function(e,a,t){e[t?0:1].push(a)},function(){return[[],[]]}),le=ie;const ce=_(le),ge={"gpt-4o":"High-intelligence flagship model for complex, multi‑step tasks","gpt-4o-mini":"Affordable and intelligent small model for fast, lightweight tasks"},de=new Set(["gpt-4o","gpt-4o-mini","gpt-4-turbo","gpt-3.5-turbo","gpt-4","gpt-4-32k","gpt-3.5-turbo-instruct"]),pe=100;function ue({value:e,onChange:a,completionMode:t,align:i,variant:s="fill",usesQueryParams:o=!0,isDisabled:l=!1,menuWidth:b=250}){const{activeOrgId:h,activeProjId:v}=M(),{engineOptions:c,isLoading:E}=V(h,v,{includeFineTunedModels:!0});m.useEffect(()=>{e&&c.length&&!c.find(d=>d.id===e)&&a(k(c,t))},[c,t]);const A=m.useMemo(()=>{const d=F(c,t),r=se(d,n=>H(n));return Object.values(x).map(n=>{var I;const O=[x.GPT3_5,x.CHAT].includes(n)?"descending":"ascending",y=((I=r[n])!=null?I:[]).map(f=>({...f,label:f.id,value:f.id}));return{label:n,options:y,sortDirection:O}})},[c,t]);return u.jsx(me,{isDisabled:l,menuWidth:b,variant:s,align:i,value:e,onChange:a,isLoading:E,engineGroups:A,playground:t,usesQueryParams:o})}const fe=({label:e})=>u.jsx("span",{className:"font-medium",children:e});function me({value:e,onChange:a,engineGroups:t,align:i,usesQueryParams:s,isLoading:o,playground:l,variant:b="fill",isDisabled:h=!1,menuWidth:v=240,layersCompatibilityMode:c=!1}){const E=m.useMemo(()=>o?[]:t.filter(r=>r.options.length>0).map(r=>{var j;const n=r.options.slice(0);((j=r.sortDirection)!=null?j:"ascending")==="ascending"?n.sort((g,p)=>g.value.localeCompare(p.value)):n.sort((g,p)=>p.value.localeCompare(g.value));const[S,y]=ce(n,g=>de.has(g.value)),f=[...S,...y].map(g=>{const p=ge[g.value];return{...g,description:p&&u.jsx("div",{className:"opacity-70 font-normal",style:{marginTop:2,fontSize:"12px"},children:p})}});return{label:r.label,options:f,optionsLimit:{limit:pe,label:"Show more"}}}),[o,t]),A=m.useCallback(r=>{var n;r.value!==e&&(w.dashboardEvent({name:C.playgroundChangeModel,data:{modelSelected:(n=r==null?void 0:r.value)!=null?n:void 0,playground:l}}),s&&D({model:r==null?void 0:r.value}),a(r))},[e,a,s,l]),d=m.useMemo(()=>{const r=t.flatMap(n=>n.options);if(!o){if(r.length===0)return"No eligible models available.";if(e&&!r.some(n=>n.value===e))return"The selected model is not available."}},[o,t,e]);return u.jsxs("div",{className:"engine-select",children:[u.jsx($,{variant:b,value:e!=null?e:"",side:"bottom",options:E,searchPlaceholder:"Select a model...",onChange:A,listMinWidth:v,align:i,TriggerView:fe,disabled:h,loading:o,layersCompatibilityMode:c}),d&&u.jsx("div",{className:"engine-select-error-message",children:d})]})}const Ee=G.memo(ue);export{Ee as E,me as G};
