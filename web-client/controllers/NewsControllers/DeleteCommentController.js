import { requester } from '../../utils/requster.js';

export function DeleteCommentController(newsId, commentId) {
    let commentToDeleteUrl = `http://127.0.0.1:8000/api/news/${newsId}/comments/${commentId}/`;

    requester.delete(commentToDeleteUrl)
        .then(() => {
            toastr.success('Comment deleted successfully!');
            window.location.href = `#/news/${newsId}`;
        }).catch((err) => {
            toastr.error('Couldn\'t delete the selected comment!');
            window.location.href = `#/news/${newsId}`;
        });
}