import {PIXIDuelView} from './duel-view'
import {PIXIMenu} from './menu-view'
import {IPresenter, IView, IViewManager, IDuelView, IMenu,
        ViewAction} from '../mvp'

export class ViewFactory {
    public create(view_type: string, presenter: IPresenter,
                  container: HTMLElement): IViewManager {
        if (view_type == 'PIXI') {
            return new PixiView(presenter, container as HTMLCanvasElement);
        }
        throw new TypeError(`No view type ${view_type}`)
    }
}

class PixiView implements IViewManager {
    private renderer: PIXI.Renderer;
    private stage: PIXI.Container;
    private ticker: PIXI.Ticker;
    private presenter: IPresenter;

    constructor(presenter: IPresenter, container: HTMLCanvasElement) {
        this.presenter = presenter;
        const app = new PIXI.Application({
            view: container,
            resizeTo: window,
            backgroundColor: 0x272D37,
        })
        this.renderer = app.renderer;
        this.stage = app.stage;
        this.ticker = app.ticker;
        this.ticker.start();
    }

    private animation(): void {
        var t = new PIXI.Text('welcome', {fontFamily: 'Arial', fontSize: 40})
        t.x = this.renderer.width / 2;
        t.y = this.renderer.height / 2;
        t.anchor.set(0.5);
        this.stage.addChild(t);
        
        var y_pos = 0;
        var initial_y = this.renderer.height / 2;
        function animate(){
            t.y = initial_y + Math.sin(y_pos) * 30;
            y_pos += 0.1;
        }

        this.ticker.add(animate);
    }

    public duelView(): IDuelView {
        var x = this.renderer.width / 2;
        var y = this.renderer.height / 2;
        var dv = new PIXIDuelView(this, x, y);
        this.stage.addChild(dv);
        return dv;
    }

    public menuView(): IMenu {
        var x = this.renderer.width / 2;
        var y = this.renderer.height / 2;
        var menu = new PIXIMenu(this, x, y);
        this.stage.addChild(menu);
        return menu;
    }

    public getPresenter(): IPresenter {
        return this.presenter;
    }

    public accept(action: ViewAction){
        this.presenter.accept(action);
    }
}


