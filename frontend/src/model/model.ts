import {IModel, IPresenter, ModelAction} from '../mvp'

export class ModelFactory {
    public create(model_type: string, presenter: IPresenter): IModel {
        if (model_type == 'LOCAL')
            return new LocalModel(presenter);
        throw new TypeError(`No model type ${model_type}`);
    }
}

// model to use when server and player are in the same network
class LocalModel implements IModel {
    private presenter: IPresenter;
    private readonly endpoint = 'http://127.0.0.1:5000';
    private soc: SocketIOClient.Socket;
    private entry: SocketIOClient.Socket;

    constructor(presenter: IPresenter) {
        this.presenter = presenter;
        this.soc = io('');
        this.entry = io(this.endpoint);

        this.entry.on('login', (player_id: number) => {
            this.soc = io(this.endpoint + '/data' + player_id);
            this.soc.on('start', (data: string) => {
                this.presenter.acceptData(ModelAction.RENDER_ALL, data);
            });
            this.soc.on('change', (data: string) => {
                this.presenter.acceptData(ModelAction.RENDER_CHANGE, data);
            });
            this.soc.on('connect', () => {
                this.entry.emit('logged_in', {'id': player_id});
            });
        });
    }

    public getPresenter(): IPresenter {
        return this.presenter;
    }

    public startSoloGame(): void {
        this.entry.emit('login');
    }

    public sendLetter(letter: string): void {
        this.soc.emit('type', {'key': letter});
    }

    public removeLetter(): void {
        this.soc.emit('remove');
    }

    public publishWord(): void {
        this.soc.emit('publish');
    }
}
