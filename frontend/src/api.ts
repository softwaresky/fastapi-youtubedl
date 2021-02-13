import axios from 'axios';
import {apiUrl} from '@/env';
import {YdlItemState, YdlItemCreate, YdlItemUpdate} from '@/store/ytdl_item/state';

export const api = {

    async getYdlItems() {
        return axios.get<YdlItemState[]>(`${apiUrl}/api/v1/youtube-dl/`);
    },
    async createYdlItem(data: YdlItemCreate) {
        return axios.post(`${apiUrl}/api/v1/youtube-dl/`, data);
    },
    async updateYdlItem(id: number, data: YdlItemUpdate) {
        return axios.put(`${apiUrl}/api/v1/youtube-dl/${id}`, data);
    },
    async removeYdlItem(id: number) {
        return axios.delete(`${apiUrl}/api/v1/youtube-dl/${id}`);
    },
}