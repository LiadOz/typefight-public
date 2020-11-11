import {IMenu, ViewAction, IViewManager} from '../mvp'
export class PIXIMenu extends PIXI.Container implements IMenu {
    private readonly WIDTH = 550;
    private readonly HEIGHT = 820;
    private x_pos: number;
    private y_pos: number;
    private manager: IViewManager;
    
    constructor(manager: IViewManager, x: number, y: number) {
        super();
        this.manager = manager;
        this.x_pos = x;
        this.y_pos = y;
        this.initBase();
        this.setTitle('typefight');
        this.addGames();
    }

    private initBase(): void {
        var graphics = new PIXI.Graphics();
        this.addChild(graphics);
        graphics.x = this.x_pos;
        graphics.y = this.y_pos;
        
        graphics.lineStyle(0);
        graphics.beginFill(0x38404E);
        graphics.drawShape(
            new PIXI.Rectangle(
                0 - this.WIDTH/2, 0 - this.HEIGHT/2, this.WIDTH, this.HEIGHT));
        graphics.endFill();

    }

    private setTitle(titleName: string): void {
        var title = new PIXI.Text(
            titleName, {fontFamily: 'monospace', fontSize:70});
        title.x = this.x_pos;
        title.y = this.y_pos - this.HEIGHT / 3;
        title.anchor.set(0.5);
        this.addChild(title)
    }

    private addGames(): void {
        var game = new PIXI.Text(
            'single player', {fontFamily: 'monospace', fontSize:30});
        game.x = this.x_pos;
        game.y = this.y_pos;
        game.anchor.set(0.5);

        game.buttonMode = true;
        game.interactive = true;
        game.on('pointerdown', () => {
            this.manager.accept(ViewAction.START_SOLO);
        });
        this.addChild(game);
    }

    public remove(): void {
        this.destroy();
    }

    public getManager(): IViewManager {
        return this.manager;
    }
}
