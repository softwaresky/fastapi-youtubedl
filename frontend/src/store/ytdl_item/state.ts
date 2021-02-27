export interface YdlItemState {
    id: number;
    url: string;
    do_calculate_pattern: boolean;
    status: number;
    timestamp: string;
    ydl_opts: object | null;
    output_log: object | null;
}

export interface YdlItemCreate {
    url: string;
    do_calculate_pattern?: boolean;
    status?: number;
    timestamp?: string;
    ydl_opts?: object | null;
    output_log?: object | null;
}

export interface YdlItemUpdate {
    url: string;
    do_calculate_pattern?: boolean;
    status?: number;
    timestamp?: string;
    ydl_opts?: object | null;
    output_log?: object | null;
}

export interface YdlUrlInfoCreate {
    url: string;
    ydl_opts?: object | null;
}

export interface YdlItemListState {
    ydlItems: YdlItemState[];
    ydlUrlInfo: {} | null;
}
