import { IDuelView, IViewManager} from '../mvp'

export class PIXIDuelView extends PIXI.Container implements IDuelView {
    private readonly DISTANCE = 30;
    private manager: IViewManager;
    private player: PlayerView;
    private rival: PlayerView;
    constructor(manager: IViewManager, x: number, y: number){
        super();
        this.manager = manager;
        var dist = PlayerView.WIDTH / 2 + this.DISTANCE / 2;
        this.player = new PlayerView(x - dist, y);
        this.rival = new PlayerView(x + dist, y)

        this.addChild(this.player);
        this.addChild(this.rival);
    }

    public renderGame(data: any): void {
        if (data.PLAYER != undefined)
            this.player.renderPlayer(data.PLAYER);
        if (data.RIVAL != undefined)
            this.rival.renderPlayer(data.RIVAL);
    }

    public renderChanges(data: any): void {
        if (data.PLAYER != undefined)
            this.player.renderChanges(data.PLAYER);
        if (data.RIVAL != undefined)
            this.rival.renderChanges(data.RIVAL);
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
    public static readonly PADDING = 5;
    private pos_x: number; // x position of center
    private pos_y: number; // y position of center
    private x_start: number;
    private y_start: number;
    private attack: AttackView;
    private defend: DefendView;
    private currLabel: PIXI.Text;
    
    constructor(pos_x: number, pos_y: number){
        super();
        this.pos_x = pos_x;
        this.pos_y = pos_y;
        this.x_start = pos_x - PlayerView.WIDTH / 2;
        this.y_start = pos_y - PlayerView.HEIGHT / 2;

        this.initBase();

        this.currLabel = new PIXI.Text(
            '', {fontFamily: 'monospace', fontSize: 50});
        this.currLabel.x = pos_x;
        this.currLabel.y = this.y_start + DefendView.HEIGHT + 10;
        this.currLabel.anchor.x = 0.5;
        this.addChild(this.currLabel);

        this.attack = new AttackView(
            this.x_start + PlayerView.PADDING,
            this.y_start + PlayerView.HEIGHT - AttackView.HEIGHT - PlayerView.PADDING);
        this.addChild(this.attack);
        this.defend = new DefendView(
            this.x_start + PlayerView.PADDING,
            this.y_start + PlayerView.PADDING);
        this.addChild(this.defend);
    }

    private initBase(): void {
        var graphics = new PIXI.Graphics();
        this.addChild(graphics);
        graphics.x = this.x_start;
        graphics.y = this.y_start;
        
        graphics.lineStyle(0);
        graphics.beginFill(0x38404E);
        graphics.drawShape(
            new PIXI.Rectangle(0, 0, PlayerView.WIDTH, PlayerView.HEIGHT));
        graphics.endFill();

    }

    public renderPlayer(data: any): void {
        if ('DEFEND' in data){
            var lines = data.DEFEND as string[];
            for (const line of lines)
                this.defend.addLine(line);
        }
        if ('ATTACK' in data) {
            var words = data.ATTACK as string[];
            for (const word of words)
                this.attack.addWord(word);
        }
        if ('CURRENT' in data) {
            this.currLabel.text = data.CURRENT;
        }
    }

    public renderChanges(data: any): void  {
        var changes = data as [string, string][];
        for (const change of changes)
            this.renderChange(change[0], change[1]);
    }

    private renderChange(c_type: string, change: string): void {
        switch (c_type) {
            case 'ADD_DEFEND':
                this.defend.addLine(change);
                break;
            case 'REMOVE_DEFEND':
                this.defend.removeWord(change);
                break;
            case 'ADD_ATTACK':
                this.attack.addWord(change);
                break;
            case 'REMOVE_ATTACK':
                this.attack.removeWord(change);
                break;
            case 'ADD_LETTER':
                this.currLabel.text += change;
                break;
            case 'REMOVE_LETTER':
                this.currLabel.text = this.currLabel.text.slice(0, -1);
                break;
            case 'CLEAR_WORD':
                this.currLabel.text = '';
                break;
        }
    }

}

class AttackView extends PIXI.Container {
    public static readonly WIDTH = 540;
    public static readonly HEIGHT = 130;
    private attackGrid: AttackGrid;
    private x_start: number;
    private y_start: number;
    
    constructor(x_start: number, y_start: number) {
        super();
        this.x_start = x_start;
        this.y_start = y_start;

        var attack = new PIXI.Graphics();
        this.addChild(attack);
        
        attack.lineStyle(3);
        attack.beginFill(0xffffff);
        attack.drawShape(
            new PIXI.Rectangle(0 , 0, AttackView.WIDTH, AttackView.HEIGHT));
        attack.endFill();
        attack.x = this.x_start;
        attack.y = this.y_start;

        this.attackGrid = new AttackGrid(
            2, 5, AttackView.WIDTH, AttackView.HEIGHT);
        this.attackGrid.x = x_start;
        this.attackGrid.y = y_start;
        this.addChild(this.attackGrid);
    }

    public addWord(word: string) {
        this.attackGrid.addWord(word);
    }

    public removeWord(word: string) {
        this.attackGrid.removeWord(word);
    }
        
}

class AttackGrid extends PIXI.Container {
    private words: Map<string, [number, PIXI.Container]>;
    private wordsPerLine: number;
    private lines: number;
    private freeCells: number[];
    private wordWidth: number;
    private wordHeight: number;

    constructor(wordsPerLine: number, lines: number,
                parentWidth: number, parentHeight: number) {
        super();
        this.wordsPerLine = wordsPerLine;
        this.lines = lines;
        this.words = new Map<string, [number, PIXI.Container]>();
        this.wordWidth = parentWidth / wordsPerLine;
        this.wordHeight = parentHeight / lines;

        this.freeCells = [];
        for (var i = 0; i < wordsPerLine * lines; i++)
            this.freeCells.push(i);
    }

    public addWord(word: string) {
        const cell = this.freeCells.pop()!;
        const x = cell % this.wordsPerLine;
        const y = Math.floor(cell / this.wordsPerLine);
        const wordSprite = new PIXI.Text(
            word, {fontFamily: 'monospace', fontSize: 15});
        wordSprite.x = this.wordWidth * x;
        wordSprite.y = this.wordHeight * y;
        this.addChild(wordSprite);
        this.words.set(word, [cell, wordSprite]);
    }

    public removeWord(word: string) {
        var prev = this.words.get(word)!;
        prev[1].destroy();
        this.freeCells.push(prev[0]);
    }
}

class DefendView extends PIXI.Container {
    public static readonly WIDTH = 540;
    public static readonly HEIGHT = 600; // original is 660
    private grid: WordGrid;
    private x_start: number;
    private y_start: number;
    
    constructor(x_start: number, y_start: number) {
        super();
        this.x_start = x_start;
        this.y_start = y_start;

        var defend = new PIXI.Graphics();
        this.addChild(defend);
        
        defend.beginFill(0xffffff);
        defend.drawShape(
            new PIXI.Rectangle(0 , 0, DefendView.WIDTH, DefendView.HEIGHT));
        defend.endFill();
        defend.x = this.x_start;
        defend.y = this.y_start;
        this.grid = new WordGrid(this.x_start, this.y_start,
                                 DefendView.WIDTH, DefendView.HEIGHT);
        // this.grid.drawGrid();
        this.addChild(this.grid);
    }

    public addLine(line: string): void {
        this.grid.addLine(line);
    }

    public removeWord(word: string): void {
        this.grid.removeWord(word);
    }
        
    
}

class WordGrid extends PIXI.Container {
    public static readonly CHARS = 40;
    public static readonly LINES = 20;
    private x_start: number;
    private y_start: number;
    private cellWidth: number;
    private cellHeight: number;
    private words: Map<string, PIXI.Container[]>;
    private wordsContainer: PIXI.Container;

    constructor(x_start: number, y_start: number,
                parentWidth: number, parentHeight: number) {
        super();
        this.x_start = x_start;
        this.y_start = y_start;
        this.cellWidth = parentWidth / WordGrid.CHARS;
        this.cellHeight = parentHeight / WordGrid.LINES;
        this.words = new Map<string, PIXI.Container[]>();
        var wc = new PIXI.Container();
        this.wordsContainer = wc;
        this.addChild(wc);
    }

    public drawGrid(): void {
        var draw = new PIXI.Graphics();
        this.addChild(draw);
        draw.beginFill(0xffffff);
        draw.x = this.x_start;
        draw.y = this.y_start;
        draw.lineStyle(2);
        for (var i = 0; i < WordGrid.LINES; i++){
            for (var j = 0; j < WordGrid.CHARS; j++){
                draw.drawShape(
                    new PIXI.Rectangle(j * this.cellWidth, i * this.cellHeight,
                                       this.cellWidth, this.cellHeight));
            }
        }
        draw.endFill();
    }

    public addLine(line: string): void {
        var splitted = line.split("#").filter(function (el) {
            return el != "";
        });
        this.shiftLine();
        var i = 0;
        var prevSep = false;
        var currWord = 0;
        var curSprites: PIXI.Text[] = [];
        while (i < WordGrid.CHARS) {
            if (line.charAt(i) == '#') {
                i++;
                if (prevSep)
                    continue;
                else {
                    this.words.set(splitted[currWord], curSprites);
                    currWord++;
                    curSprites = [];
                    prevSep = true;
                    continue;
                }
            }
            const letterSprite = new PIXI.Text(
                line.charAt(i), {fontFamily: 'monospace', fontSize: 30});
            letterSprite.width = this.cellWidth;
            letterSprite.height = this.cellHeight;
            letterSprite.y = this.y_start;
            letterSprite.x = this.x_start + (i * this.cellWidth);
            curSprites.push(letterSprite);
            this.wordsContainer.addChild(letterSprite);
            i++;
            prevSep = false;
        }
        // insert last word
        this.words.set(splitted[currWord], curSprites);
    }

    public shiftLine(): void {
        for (var i = 0; i < this.wordsContainer.children.length; i++){
            this.wordsContainer.children[i].y += this.cellHeight;
        }
    }

    public removeWord(word: string): void {
        this.words.get(word)?.forEach(function (sp) {
            sp.destroy();
        })
    }
}
