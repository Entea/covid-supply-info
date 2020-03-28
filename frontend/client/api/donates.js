import {ApiClient} from '../client';

let client = new ApiClient();

export default {
    all() {
        return client.get('/donations');
    }
};

