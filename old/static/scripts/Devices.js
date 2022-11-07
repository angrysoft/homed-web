export { Device };
import { DeviceModel } from "./DevicesModel.js";
import { DeviceView } from "./DevicesView.js";
import { TraitsFactory } from "./Traits/TraitsFactory.js";
class Device {
    constructor(deviceInfo) {
        this.model = new DeviceModel(deviceInfo);
        this.view = new DeviceView(this.model.sid, this.model.name, this.model.place);
        this.loadTraits();
        this.updateStatus(deviceInfo);
        this.view.render();
    }
    loadTraits() {
        this.model.traitsNames.forEach(trait => {
            let traitView = TraitsFactory.getTrait(trait);
            if (traitView != undefined) {
                this.view.addTraitView(traitView);
                this.model.registerTraitStatus(traitView);
                this.commandHandler(traitView);
            }
        });
    }
    commandHandler(trait) {
        if (trait.sendCommands) {
            trait.addEventListener("send-command", (cmd) => {
                console.log(cmd.detail);
                let event = {
                    'event': `execute.${this.model.sid}.${cmd.detail[0]}.${cmd.detail[1]}`,
                    'args': cmd.detail
                };
                fetch(`${document.location.origin}/devices/send`, { method: 'POST', body: JSON.stringify(event) });
            });
        }
    }
    async updateStatus(status) {
        for (let key in status) {
            if (key === '_id' || key === '_rev') {
                continue;
            }
            await this.model.update(key, status[key]);
        }
    }
    getView() {
        return this.view;
    }
    get sid() {
        return this.model.sid;
    }
}
