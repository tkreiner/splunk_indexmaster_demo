"use strict";(self.webpackChunk_splunk_ucc_ui_lib=self.webpackChunk_splunk_ucc_ui_lib||[]).push([[987],{2987:(e,t,n)=>{n.r(t),n.d(t,{default:()=>ye});var r=n(7294),o=n(9250),a=n(1569),i=n.n(a),u=n(2788),l=n(1946),c=n.n(l),s=n(2672),f=n.n(s),p=n(6219),m=n(4695),b=n(2681),y=n(3392),d=n(6188),v=n(3433),g=n(3985),h=n(5697),S=n.n(h),O=n(6635),j=n.n(O),w=n(2725),E=n.n(w),N=n(7354),P=n.n(N),_=n(720),C=n.n(_),k=n(5947),I=n(3137),T=n(7123);function R(e){return R="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},R(e)}function A(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,L(r.key),r)}}function D(e,t,n){return t=q(t),function(e,t){if(t&&("object"===R(t)||"function"==typeof t))return t;if(void 0!==t)throw new TypeError("Derived constructors may only return object or undefined");return z(e)}(e,M()?Reflect.construct(t,n||[],q(e).constructor):t.apply(e,n))}function M(){try{var e=!Boolean.prototype.valueOf.call(Reflect.construct(Boolean,[],(function(){})))}catch(e){}return(M=function(){return!!e})()}function q(e){return q=Object.setPrototypeOf?Object.getPrototypeOf.bind():function(e){return e.__proto__||Object.getPrototypeOf(e)},q(e)}function z(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function x(e,t){return x=Object.setPrototypeOf?Object.setPrototypeOf.bind():function(e,t){return e.__proto__=t,e},x(e,t)}function Z(e,t,n){return(t=L(t))in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function L(e){var t=function(e,t){if("object"!=R(e)||!e)return e;var n=e[Symbol.toPrimitive];if(void 0!==n){var r=n.call(e,"string");if("object"!=R(r))return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return String(e)}(e);return"symbol"==R(t)?t:String(t)}var B=function(e){function t(e){var n;return function(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}(this,t),Z(z(n=D(this,t,[e])),"setValue",(function(e){n.props.handleChange(e)})),Z(z(n),"loadCustomMenu",(function(){return new Promise((function(e){if("external"===n.props.type)import("".concat((0,T.a)(),"/custom/").concat(n.props.fileName,".js")).then((function(t){var n=t.default;e(n)}));else{var t=(0,m.YK)().meta.name;require(["app/".concat(t,"/js/build/custom/").concat(n.props.fileName)],(function(t){return e(t)}))}}))})),n.state={loading:!0},n.shouldRender=!0,n}var n,o;return function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),Object.defineProperty(e,"prototype",{writable:!1}),t&&x(e,t)}(t,e),n=t,(o=[{key:"componentDidMount",value:function(){var e=this,t=(0,m.YK)(),n=t.pages.inputs,r=n.services,o=n.menu,a=n.groupsMenu;this.setState({loading:!0}),this.loadCustomMenu().then((function(n){var i=new n(t,e.el,e.setValue);r&&o&&!a&&i.render(),e.setState({loading:!1})}))}},{key:"shouldComponentUpdate",value:function(e,t){return!(t.loading||!this.shouldRender||(this.shouldRender=!1,0))}},{key:"render",value:function(){var e=this;return r.createElement(r.Fragment,null,this.state.loading&&(0,p._)("Loading..."),r.createElement("span",{ref:function(t){e.el=t},style:{visibility:this.state.loading?"hidden":"visible"}}))}}])&&A(n.prototype,o),Object.defineProperty(n,"prototype",{writable:!1}),t}(r.Component);B.propTypes={fileName:S().string.isRequired,type:S().string,handleChange:S().func};const F=B;var K,U=n(2054),Y="Invariant failed";function V(e,t){if(!e){var n=t?"".concat(Y,": ").concat(t):Y;throw new Error(n)}}function $(e){return $="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},$(e)}function G(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var n=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null!=n){var r,o,a,i,u=[],l=!0,c=!1;try{if(a=(n=n.call(e)).next,0===t){if(Object(n)!==n)return;l=!1}else for(;!(l=(r=a.call(n)).done)&&(u.push(r.value),u.length!==t);l=!0);}catch(e){c=!0,o=e}finally{try{if(!l&&null!=n.return&&(i=n.return(),Object(i)!==i))return}finally{if(c)throw o}}return u}}(e,t)||function(e,t){if(e){if("string"==typeof e)return H(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?H(e,t):void 0}}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function H(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}var W,J,Q=u.default.span(K||(W=["\n    color: ",";\n    font-size: ",";\n    font-weight: 500;\n"],J||(J=W.slice(0)),K=Object.freeze(Object.defineProperties(W,{raw:{value:Object.freeze(J)}}))),k.variables.brandColorD20,k.variables.fontSizeSmall),X="main_panel";function ee(e){var t=e.handleRequestOpen,n=G((0,r.useState)(X),2),o=n[0],a=n[1],i=G((0,r.useState)("forward"),2),u=i[0],l=i[1],c=G((0,r.useState)(!1),2),s=c[0],f=c[1],b=G((0,r.useState)(!0),2),y=b[0],d=b[1],v=(0,m.YK)().pages.inputs;V(v);var g="groupsMenu"in v?v.groupsMenu:void 0,h="menu"in v?v.menu:void 0,S=v.services,O=["clickAway","escapeKey","offScreen","toggleClick"],w=r.createElement(U.Sn,{appearance:"primary",id:"addInputBtn",label:(0,p._)("Create New Input"),isMenu:!0});(0,r.useEffect)((function(){y||(f(!1),d(!0))}),[y]);var N,_=function(e){var t=e.reason;f(!O.includes(t))},k=function(){f(!0)},T=function(e){var n=e.service,r=e.input;t({serviceName:n,input:r})},R=(0,r.useMemo)((function(){var e,n,o,i,u=(e={},o=[],i=function(e,t){if("object"!=$(e)||!e)return e;var n=e[Symbol.toPrimitive];if(void 0!==n){var r=n.call(e,"string");if("object"!=$(r))return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return String(e)}(n=X),(n="symbol"==$(i)?i:String(i))in e?Object.defineProperty(e,n,{value:o,enumerable:!0,configurable:!0,writable:!0}):e[n]=o,e);return g?g.forEach((function(e){var t;null!=e&&e.groupServices?(u[e.groupName]=[],e.groupServices.forEach((function(t){var n,r;u[e.groupName].push({name:t,hasSubmenu:!1,title:(null===(n=S.find((function(e){return e.name===t})))||void 0===n?void 0:n.title)||"",subTitle:null===(r=S.find((function(e){return e.name===t})))||void 0===r?void 0:r.subTitle})})),u[X].push({name:e.groupName,title:e.groupTitle,hasSubmenu:!0})):u[X].push({name:e.groupName,title:e.groupTitle,subTitle:null===(t=S.find((function(t){return t.name===e.groupName})))||void 0===t?void 0:t.subTitle,hasSubmenu:!1})})):u[X]=S.map((function(e){return{name:e.name,title:e.title,subTitle:e.subTitle,hasSubmenu:!1}})),function(e){return Object.keys(e).map((function(n){return r.createElement(P().Panel,{key:n,panelId:n},r.createElement(E(),null,n!==X&&r.createElement(r.Fragment,null,r.createElement(E().Item,{icon:r.createElement(C(),null),onClick:function(){a(X),l("backward")}},"Back"),r.createElement(E().Divider,null)),(o=e[n],i=n,o.map((function(e){return null!=e&&e.hasSubmenu?r.createElement(E().Item,{hasSubmenu:!0,key:e.name,onClick:function(){a(e.name),l("forward")}},e.title):r.createElement(E().Item,{key:e.name,onClick:function(){t({serviceName:e.name,groupName:i}),d(!1)}},e.title,r.createElement(Q,null," ",e.subTitle))})))));var o,i}))}(u)}),[]),A=function(){return r.createElement(j(),{toggle:w,open:s,onRequestClose:_,onRequestOpen:k},r.createElement(P(),{activePanelId:o,transition:u,style:{width:"210px"}},R))},D=function(){return r.createElement(U.Sn,{label:(0,I.P)(100),appearance:"primary",id:"addInputBtn",onClick:function(){t({serviceName:S[0].name})}})};return!S||null!=h&&h.src?S&&null!=h&&h.src&&g?(N=h,r.createElement(r.Fragment,null,r.createElement(F,{fileName:N.src,type:N.type,handleChange:T}),1===S.length?D():A())):(V(h),function(e){return r.createElement(r.Fragment,null,r.createElement(F,{fileName:e.src,type:e.type,handleChange:T}))}(h)):1===S.length?D():A()}ee.propTypes={handleRequestOpen:S().func};const te=ee;var ne,re=n(1838),oe=n(5354),ae=n(775),ie=n(9190),ue=n(226),le=n(6622);function ce(e){return ce="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},ce(e)}function se(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function fe(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?se(Object(n),!0).forEach((function(t){var r,o,a,i;r=e,o=t,a=n[t],i=function(e,t){if("object"!=ce(e)||!e)return e;var n=e[Symbol.toPrimitive];if(void 0!==n){var r=n.call(e,"string");if("object"!=ce(r))return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return String(e)}(o),(o="symbol"==ce(i)?i:String(i))in r?Object.defineProperty(r,o,{value:a,enumerable:!0,configurable:!0,writable:!0}):r[o]=a})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):se(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function pe(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var n=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null!=n){var r,o,a,i,u=[],l=!0,c=!1;try{if(a=(n=n.call(e)).next,0===t){if(Object(n)!==n)return;l=!1}else for(;!(l=(r=a.call(n)).done)&&(u.push(r.value),u.length!==t);l=!0);}catch(e){c=!0,o=e}finally{try{if(!l&&null!=n.return&&(i=n.return(),Object(i)!==i))return}finally{if(c)throw o}}return u}}(e,t)||function(e,t){if(e){if("string"==typeof e)return me(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?me(e,t):void 0}}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function me(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}var be=(0,u.default)(i().Row)(ne||(ne=function(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}(["\n    padding: 5px 0px;\n\n    .title_menu_column {\n        width: auto !important;\n    }\n\n    .page_subtitle {\n        min-height: 20px;\n    }\n\n    .dropdown {\n        text-align: right;\n    }\n"])));const ye=function(){var e=pe((0,r.useState)({open:!1}),2),t=e[0],n=e[1],a=(0,m.YK)().pages.inputs,u=a.services,l=a.title,s=a.table,h=a.description,S=a.subDescription,O=!s,j=pe((0,r.useState)(u[0].name),2),w=j[0],E=j[1],N=u.find((function(e){return e.name===w})),P=[d.Oh,d.jg,d.bZ],_=u.map((function(e){return e.name})),C=(0,o.s0)(),k=(0,le.Z)();(0,r.useEffect)((function(){I(),T()}),[(0,o.TH)().search]);var I=function(){var e=u.find((function(e){return e.name===k.get("service")}));k&&e&&P.includes(k.get("action"))&&!t.open?k.get("action")!==d.jg&&t.stanzaName?n(fe(fe({},t),{},{open:!0,isInputPageStyle:!0,serviceName:k.get("service"),mode:k.get("action")})):n(fe(fe({},t),{},{open:!0,isInputPageStyle:!0,serviceName:k.get("service"),formLabel:"Create ".concat(null==e?void 0:e.title),mode:d.jg})):k.get("service")&&k.get("action")||!t.open||!t.isInputPageStyle||n(fe(fe({},t),{},{open:!1}))},T=function(){k&&_.includes(k.get("service"))&&E(k.get("service"))},R=function(e){var r=e.serviceName,o=e.groupName,a=e.input,i=u.find((function(e){return e.name===r})),l=i.title,c=i.style===g.G;if(n(fe(fe({},t),{},{open:!0,serviceName:r,mode:d.jg,formLabel:"Add ".concat(l),isInputPageStyle:c,groupName:o})),c){k.set("service",r),k.set("action",d.jg);var s=a||(o&&o!==X?o:null)||r;s?k.set("input",s):k.delete("input"),C({search:k.toString()})}},A=function(e,r){var o,a=null===(o=u.find((function(t){return t.name===e.serviceName})))||void 0===o?void 0:o.title;n(fe(fe({},t),{},{open:!0,isInputPageStyle:!0,serviceName:e.serviceName,stanzaName:e.name,formLabel:r===d.Oh?"Clone ".concat(a):"Update ".concat(a),mode:r})),k.set("service",e.serviceName),k.set("action",r),C({search:k.toString()})},D=(0,r.useCallback)((function(e,t){var n=t.selectedTabId;E(n),k.delete("action"),k.set("service",n),C({search:k.toString()})}),[w]);return r.createElement(ae.Z,null,r.createElement(y.W,{value:null},t.isInputPageStyle&&t.open?r.createElement(ie.Z,{open:t.open,handleRequestClose:function(){n(fe(fe({},t),{},{open:!1})),O||k.delete("service"),k.delete("action"),C({search:k.toString()})},serviceName:t.serviceName,stanzaName:t.stanzaName,mode:t.mode,formLabel:t.formLabel,page:v.b,groupName:t.groupName}):null," ",r.createElement("div",{style:t.isInputPageStyle&&t.open?{display:"none"}:{display:"block"}},r.createElement(i(),{gutter:8},r.createElement(be,null,r.createElement(i().Column,{className:O&&"title_menu_column",span:9},r.createElement(b.r3,null,O?(0,p._)(N.title):(0,p._)(l||"")),r.createElement(b.pZ,{className:O&&"page_subtitle"},O?(0,p._)(N.description):(0,p._)(h||"")),r.createElement(ue.Z,S)),r.createElement(i().Column,{className:O?"title_menu_column":"dropdown",span:3},!O&&r.createElement(te,{handleRequestOpen:R})))),O?r.createElement(r.Fragment,null,r.createElement(f(),{activeTabId:w,onChange:D},u.map((function(e){return r.createElement(f().Tab,{key:e.name,label:(0,p._)(e.title),tabId:e.name})}))),u.map((function(e){return r.createElement("div",{key:e.name,style:e.name!==w?{display:"none"}:{display:"block"},id:"".concat(e.name,"Tab")},r.createElement(re.Z,{page:v.b,serviceName:e.name,handleRequestModalOpen:function(){return R({serviceName:e.name})},handleOpenPageStyleDialog:A}))}))):r.createElement(re.Z,{page:v.b,handleOpenPageStyleDialog:A,displayActionBtnAllRows:!0}),r.createElement(c(),{position:"top-right"}),!t.isInputPageStyle&&t.open?r.createElement(oe.Z,{page:v.b,open:t.open,handleRequestClose:function(){n(fe(fe({},t),{},{open:!1}))},serviceName:t.serviceName,mode:d.jg,formLabel:t.formLabel,groupName:t.groupName}):null)))}}}]);
//# sourceMappingURL=987.6f67c44f670a48c87d61.js.map