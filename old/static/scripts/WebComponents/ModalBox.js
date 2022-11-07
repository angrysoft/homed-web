import { BaseComponent } from "./BaseComponent.js";
export class ModalBox extends BaseComponent {
    constructor() {
        super();
        this.cssSheet.insertRule(`:host {
            display:none;
            grid-auto-columns: 1fr;
            position: fixed;
            z-index: 100;
            left: 0;
            top :0;
            width:100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(35,35,35,0.9);
        }`);
        this.cssSheet.insertRule(`section {
            display: grid;
            grid-row-gap: 0.5rem;
            grid-template-columns: auto;
            grid-template-rows: auto 1fr;
            align-content: center;
            
            position : relative;
            z-index: 1;
            padding: 0.5rem;
            background: black;
            color:white;
            animation-duration: .3s;
            animation-name: zoomIn;
        }`);
        this.cssSheet.insertRule(`header {
            display: grid;
            gap: 1rem;
            grid-template-columns: auto 1fr;
            padding 0.5rem;
        }`);
        this.cssSheet.insertRule(`article {
            display: grid;
            gap: 1rem;
            padding 0.5rem;
            grid-template-areas: 
            "color color color color color color"
            "colorTemp colorTemp colorTemp colorTemp colorTemp colorTemp"
            "bright bright bright bright bright bright"
            ". . arrows arrows . ."
            ". . return exit . ."
            "mediaBtn mediaBtn mediaBtn mediaBtn mediaBtn mediaBtn"
            "volume volume volume volume volume volume"
            "channel channel channel channel channel channel"
        }`);
        this.content = document.createElement("section");
        this.header = document.createElement("header");
        this.close = document.createElement("div");
        this.close.innerText = "<-";
        this.close.style.cursor = 'pointer';
        this.close.addEventListener('click', () => this.hide());
        this.headerTitle = document.createElement("div");
        this.headerTitle.innerText = "Device Options";
        this.header.appendChild(this.close);
        this.header.appendChild(this.headerTitle);
        this.body = document.createElement("article");
        this.content.appendChild(this.header);
        this.content.appendChild(this.body);
        this.root.appendChild(this.content);
    }
    show() {
        let rule = this.cssSheet.cssRules[3];
        rule.style.display = "grid";
    }
    hide() {
        let rule = this.cssSheet.cssRules[3];
        rule.style.display = "none";
    }
    set title(value) {
        this.headerTitle.innerText = value;
    }
    get title() {
        return this.headerTitle.innerText;
    }
    addBodyElement(el) {
        this.body.appendChild(el);
    }
}
window.customElements.get("modal-box") || window.customElements.define('modal-box', ModalBox);
