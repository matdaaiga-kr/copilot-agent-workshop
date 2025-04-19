import React from "react";
import styled from "styled-components";
import { useAuth } from "../../context/AuthContext";
import { commentApi } from "../../api/apiService";

// 댓글 컴포넌트
const CommentItem = ({ comment, onCommentDelete, onCommentUpdate }) => {
  const { user } = useAuth();
  const [isEditing, setIsEditing] = React.useState(false);
  const [editContent, setEditContent] = React.useState(comment.content);

  const isAuthor = user && user.userId === comment.author.id;

  // 댓글 수정 모드로 전환
  const handleEditClick = () => {
    setIsEditing(true);
    setEditContent(comment.content);
  };

  // 댓글 수정 취소
  const handleCancelEdit = () => {
    setIsEditing(false);
  };

  // 댓글 수정 저장
  const handleSaveEdit = async () => {
    if (editContent.trim() === "") return;

    try {
      await commentApi.updateComment(comment.id, editContent);
      onCommentUpdate({ ...comment, content: editContent });
      setIsEditing(false);
    } catch (error) {
      console.error("댓글 수정 중 오류 발생:", error);
    }
  };

  // 댓글 삭제
  const handleDeleteClick = async () => {
    if (window.confirm("댓글을 삭제하시겠습니까?")) {
      try {
        await commentApi.deleteComment(comment.id);
        onCommentDelete(comment.id);
      } catch (error) {
        console.error("댓글 삭제 중 오류 발생:", error);
      }
    }
  };

  return (
    <CommentContainer>
      <UserInfoContainer>
        <UserAvatar />
        <Username>{comment.author.username}</Username>
      </UserInfoContainer>

      {isEditing ? (
        <EditContainer>
          <CommentInput
            value={editContent}
            onChange={(e) => setEditContent(e.target.value)}
            autoFocus
          />
          <EditActions>
            <ActionButton onClick={handleSaveEdit}>완료</ActionButton>
            <ActionButton secondary onClick={handleCancelEdit}>
              취소
            </ActionButton>
          </EditActions>
        </EditContainer>
      ) : (
        <ContentContainer>
          <CommentContent>{comment.content}</CommentContent>

          {isAuthor && (
            <ActionButtons>
              <ActionButton onClick={handleEditClick}>수정</ActionButton>
              <ActionButton secondary onClick={handleDeleteClick}>
                삭제
              </ActionButton>
            </ActionButtons>
          )}
        </ContentContainer>
      )}
    </CommentContainer>
  );
};

// 스타일 컴포넌트
const CommentContainer = styled.div`
  display: flex;
  flex-direction: column;
  width: 100%;
  padding: 0.75rem 0;
  border-bottom: 1px solid #333;
`;

const UserInfoContainer = styled.div`
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
`;

const UserAvatar = styled.div`
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: ${(props) => props.theme.colors.gray};
  margin-right: 0.5rem;
`;

const Username = styled.div`
  font-size: ${(props) => props.theme.fontSizes.sm};
  font-weight: ${(props) => props.theme.fontWeights.bold};
  color: ${(props) => props.theme.colors.text};
`;

const ContentContainer = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
`;

const CommentContent = styled.p`
  font-size: ${(props) => props.theme.fontSizes.sm};
  color: ${(props) => props.theme.colors.text};
  line-height: 1.4;
  word-break: break-word;
  flex: 1;
`;

const ActionButtons = styled.div`
  display: flex;
  gap: 0.5rem;
`;

const ActionButton = styled.button`
  background: none;
  color: ${(props) =>
    props.secondary ? props.theme.colors.darkGray : props.theme.colors.primary};
  font-size: ${(props) => props.theme.fontSizes.xs};
  padding: 2px 4px;
  cursor: pointer;
`;

const EditContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const CommentInput = styled.textarea`
  width: 100%;
  background-color: #1a1a1a;
  border: 1px solid #333;
  border-radius: ${(props) => props.theme.sizes.borderRadius.sm};
  padding: 0.5rem;
  color: ${(props) => props.theme.colors.text};
  font-size: ${(props) => props.theme.fontSizes.sm};
  min-height: 60px;
  resize: vertical;
`;

const EditActions = styled.div`
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
`;

export default CommentItem;
