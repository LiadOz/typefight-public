export class Menu {

    private title: string;
    private buttons: MenuButton[];
    constructor(title: string) {
        this.title = title;
        this.buttons = [];
    }
    public get_title(): string {
        return this.title;
    }
    public add_button(btn: MenuButton){
        this.buttons.push(btn);
    }
}


export class MenuButton {
    private name: string;
    private action: () => void;

    constructor(btn_name: string, btn_action: () => void) {
        this.name = btn_name;
        this.action = btn_action;
    }

    public click(): void {
        console.log("clicked " + this.name);
        this.action();
    }

    public get_name(): string {
        return this.name;
    }

}
