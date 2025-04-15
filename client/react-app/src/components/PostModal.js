import React, { useState, useEffect, useRef } from 'react';
import { postService } from '../services/api';
import '../styles/PostModal.css';

const PostModal = ({ isOpen, onClose, onPostComplete }) => {
  const [content, setContent] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const modalRef = useRef(null);
  const textareaRef = useRef(null);

  // 모달이 열릴 때 텍스트 영역에 포커스
  useEffect(() => {
    if (isOpen && textareaRef.current) {
      textareaRef.current.focus();
    }
  }, [isOpen]);

  // 모달 외부 클릭 시 닫기
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (modalRef.current && !modalRef.current.contains(event.target)) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen, onClose]);

  // Esc 키 누르면 모달 닫기
  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.key === 'Escape') {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleKeyDown);
    }
    
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [isOpen, onClose]);

  // 게시글 작성 제출 처리
  const handleSubmit = async () => {
    if (!content.trim()) return;
    
    try {
      setIsSubmitting(true);
      // API 호출하여 게시글 작성
      const response = await postService.createPost(content);
      setContent('');
      // 부모 컴포넌트에게 게시글 작성 완료 알림
      onPostComplete(response);
      onClose();
    } catch (error) {
      console.error('게시글 작성 중 오류가 발생했습니다:', error);
      alert('게시글 작성 중 오류가 발생했습니다. 다시 시도해주세요.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-container" ref={modalRef}>
        <textarea
          ref={textareaRef}
          className="modal-textarea"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="내용을 입력하세요."
          maxLength={500}
        />
        
        <div className="modal-buttons">
          <button
            className="modal-button button-cancel"
            onClick={onClose}
            disabled={isSubmitting}
          >
            취소
          </button>
          
          <button
            className={`modal-button button-complete ${!content.trim() || isSubmitting ? 'button-disabled' : ''}`}
            onClick={handleSubmit}
            disabled={!content.trim() || isSubmitting}
          >
            {isSubmitting ? '처리 중...' : '완료'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default PostModal;