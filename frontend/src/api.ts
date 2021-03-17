import axios from 'axios';
import {apiUrl} from './env';
import {YdlItemState, YdlItemCreate, YdlItemUpdate, YdlUrlInfoCreate} from '@/store/ytdl_item/state';

export const api = {

    async getYdlItems() {
        return axios.get<YdlItemState[]>(`${apiUrl}/api/v1/youtube-dl/`);
    },
    async getYdlItemsData() {
        return axios.get<YdlItemState[]>(`${apiUrl}/api/v1/youtube-dl/items-data/`);
    },
    async getYdlUrlInfo(data: YdlUrlInfoCreate) {
        return axios.post(`${apiUrl}/api/v1/youtube-dl/ydl-url-info`, data);
    },
    async createYdlItem(data: YdlItemCreate) {
        return axios.post(`${apiUrl}/api/v1/youtube-dl`, data);
    },
    async updateYdlItem(id: number, data: YdlItemUpdate) {
        return axios.put(`${apiUrl}/api/v1/youtube-dl/${id}`, data);
    },
    async removeYdlItem(id: number) {
        return axios.delete(`${apiUrl}/api/v1/youtube-dl/${id}`);
    },
    async getYdlItemLog(id: number) {
        return axios.get(`${apiUrl}/api/v1/youtube-dl/object-data/${id}`);
    },
}