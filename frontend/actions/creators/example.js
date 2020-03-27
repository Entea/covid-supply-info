import * as actionTypes from '../example';

export const clickExample = (data) => {
    return { type: actionTypes.CLICK_EXAMPLE, data: data }
};