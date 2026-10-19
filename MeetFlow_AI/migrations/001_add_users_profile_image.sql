-- users 테이블에 프로필 사진 컬럼 추가
-- (create_all 은 이미 존재하는 테이블을 수정하지 않으므로 기존 DB 에는 한 번 직접 실행해야 합니다)
ALTER TABLE users ADD COLUMN IF NOT EXISTS profile_image VARCHAR(500);
