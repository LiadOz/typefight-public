import {IModel, IViewManager, IPresenter,
    ViewAction, IView, ModelAction, IDuelView} from '../mvp'
import {ViewFactory} from '../view/view'
import {ModelFactory} from '../model/model'

export class Presenter implements IPresenter {

    private model: IModel;
    private view: IViewManager;
    private currView: IView;
    constructor(container: HTMLElement){
        this.model = new ModelFactory().create('LOCAL', this);
        this.view = new ViewFactory().create('PIXI', this, container);
        this.currView = this.view.menuView();
    }

    public run(): void {
        // this.view.createMenu();
    }

    public accept(action: ViewAction){
        if (action == ViewAction.START_SOLO){
            this.currView.remove();
            this.currView = this.view.duelView();
            this.model.startSoloGame();
            this.registerKeyboard();
        }
        if (action == ViewAction.START_DUEL){
            this.currView.remove();
            this.currView = this.view.duelView();
            this.model.startDuelGame();
            this.registerKeyboard();
        }
    }

    public acceptData(action: ModelAction, data: string) {
        const payload = JSON.parse(data);
        var dv = this.currView as IDuelView;
        if (action == ModelAction.RENDER_ALL)
            dv.renderGame(payload);
        else if (action == ModelAction.RENDER_CHANGE)
            dv.renderChanges(payload);
    }

    private registerKeyboard(): void{
        document.addEventListener('keydown', (event: KeyboardEvent) => {
            if (event.key.length == 1 && event.key.match("[a-z]")){
                var pushed = event.key;
                this.model.sendLetter(pushed);
            }

            else if (event.key == 'Backspace')
                this.model.removeLetter();

            else if (event.key == ' ')
                this.model.publishWord();
        });
    }
}
