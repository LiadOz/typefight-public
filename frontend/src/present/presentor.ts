import {IModel, IViewManager, IPresenter, ViewAction, IView} from '../mvp'
import {ViewFactory} from '../view/view'
import {Model} from '../model/model'
export class Presenter implements IPresenter {

    private model: IModel;
    private view: IViewManager;
    private currView: IView;
    constructor(container: HTMLElement){
        this.model = new Model;
        this.view = new ViewFactory().create('PIXI', this, container);
        this.currView = this.view.menuView();
    }

    public run(): void {
        this.registerKeyboard();
        // this.view.createMenu();
    }

    public accept(action: ViewAction){
        if (action == ViewAction.START_SOLO){
            this.currView.remove();
            this.currView = this.view.duelView();
        }
    }

    private registerKeyboard(): void{
        document.addEventListener('keydown', (event: KeyboardEvent) => {
            if (event.key.length == 1 && event.key.match("[a-z]")){
                console.log(event.key);
            }
        });
    }
}
