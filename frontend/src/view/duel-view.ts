import { IDuelView, IViewManager} from '../mvp'

export class PIXIDuelView extends PIXI.Container implements IDuelView {
    private readonly DISTANCE = 30;
    private manager: IViewManager;
    constructor(manager: IViewManager, x: number, y: number){
        super();
        this.manager = manager;
        var dist = PlayerView.WIDTH / 2 + this.DISTANCE / 2;
        this.addChild(new PlayerView(x - dist, y));
        this.addChild(new PlayerView(x + dist, y));
    }

    public addWord(): void {
        
    }

    public removeWord(): void {
        
    }

    public remove(): void {
        this.destroy();
    }

    public getManager(): IViewManager {
        return this.manager;
    }
}

class PlayerView extends PIXI.Container {
    public static readonly WIDTH = 550;
    public static readonly HEIGHT = 820
    private pos_x: number;
    private pos_y: number;
    
    constructor(pos_x: number, pos_y: number){
        super();
        this.pos_x = pos_x;
        this.pos_y = pos_y;
        this.initBase();
    }

    private initBase(): void {
        var graphics = new PIXI.Graphics();
        this.addChild(graphics);
        graphics.x = this.pos_x;
        graphics.y = this.pos_y;
        
        graphics.lineStyle(0);
        graphics.beginFill(0xffffff);
        graphics.drawShape(
            new PIXI.Rectangle(
                0 - PlayerView.WIDTH/2, 0 - PlayerView.HEIGHT/2,
                PlayerView.WIDTH, PlayerView.HEIGHT));
        graphics.endFill();

        var game = new PIXI.Text(
            'the little frog jumped over the lazy cat',
            {fontFamily: 'monospace', fontSize:21});
        game.x = this.pos_x;
        game.y = this.pos_y;
        game.anchor.set(0.5);
        this.addChild(game);
    }
}
