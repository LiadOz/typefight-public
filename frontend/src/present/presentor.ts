import {ViewFactory, IView} from '../view/view'
import {Model} from '../model/model'
export class Presenter {

    private model: Model;
    private view: IView;
    constructor(container: HTMLElement){
        this.model = new Model;
        this.view = new ViewFactory().create('PIXI', container);
    }

    public run(): void {
        this.view.initView();
    }
}
