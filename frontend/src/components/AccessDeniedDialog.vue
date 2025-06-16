<template>
  <div class="access-denied-overlay" v-if="visible" @click="handleClose">
    <div class="access-denied-dialog" @click.stop>
      <!-- 科技风格边框装饰 -->
      <div class="dialog-frame">
        <!-- 顶部装饰线 -->
        <div class="frame-top">
          <div class="corner-left"></div>
          <div class="tech-line"></div>
          <div class="corner-right"></div>
        </div>
        
        <!-- 左右侧边装饰 -->
        <div class="frame-left"></div>
        <div class="frame-right"></div>
        
        <!-- 底部装饰线 -->
        <div class="frame-bottom">
          <div class="corner-left"></div>
          <div class="tech-line"></div>
          <div class="corner-right"></div>
        </div>
      </div>
      
      <!-- 弹窗内容 -->
      <div class="dialog-content">
        <!-- 警告图标 -->
        <div class="warning-icon">
          <div class="icon-glow"></div>
          <img src="/src/assets/image/警告.png" alt="警告" class="warning-image">
        </div>
        
        <!-- 标题 -->
        <h2 class="dialog-title">访问受限</h2>
        
        <!-- 内容文字 -->
        <p class="dialog-message">{{ message }}</p>
        
        <!-- 确认按钮 -->
        <button class="confirm-button" @click="handleConfirm">
          <span class="button-text">确认</span>
          <div class="button-glow"></div>
        </button>
      </div>
      
      <!-- 背景光效 -->
      <div class="dialog-effects">
        <div class="bg-glow"></div>
        <div class="particles"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'

interface Props {
  visible: boolean
  message?: string
  title?: string
}

const props = withDefaults(defineProps<Props>(), {
  message: '您没有权限访问此功能',
  title: '访问受限'
})

const emit = defineEmits<{
  close: []
  confirm: []
}>()

const handleClose = () => {
  emit('close')
}

const handleConfirm = () => {
  emit('confirm')
  emit('close')
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

/* 遮罩层 */
.access-denied-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 20, 50, 0.8);
  backdrop-filter: blur(10px);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Orbitron', monospace;
}

/* 弹窗主体 */
.access-denied-dialog {
  position: relative;
  width: 480px;
  height: 320px;
  background: linear-gradient(
    145deg,
    rgba(15, 30, 60, 0.95),
    rgba(25, 50, 100, 0.9),
    rgba(15, 30, 60, 0.95)
  );
  border-radius: 12px;
  border: 2px solid rgba(0, 150, 255, 0.4);
  backdrop-filter: blur(20px);
  box-shadow: 
    0 20px 40px rgba(0, 0, 0, 0.6),
    inset 0 1px 0 rgba(255, 255, 255, 0.1),
    0 0 30px rgba(0, 150, 255, 0.3);
  overflow: hidden;
  animation: dialogSlideIn 0.5s cubic-bezier(0.23, 1, 0.32, 1);
}

/* 科技风格边框 */
.dialog-frame {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.frame-top, .frame-bottom {
  position: absolute;
  left: 20px;
  right: 20px;
  height: 20px;
  display: flex;
  align-items: center;
}

.frame-top {
  top: 15px;
}

.frame-bottom {
  bottom: 15px;
}

.frame-left, .frame-right {
  position: absolute;
  top: 35px;
  bottom: 35px;
  width: 20px;
}

.frame-left {
  left: 15px;
  border-left: 2px solid rgba(255, 100, 100, 0.6);
  border-top: 1px solid rgba(255, 100, 100, 0.3);
  border-bottom: 1px solid rgba(255, 100, 100, 0.3);
}

.frame-right {
  right: 15px;
  border-right: 2px solid rgba(255, 100, 100, 0.6);
  border-top: 1px solid rgba(255, 100, 100, 0.3);
  border-bottom: 1px solid rgba(255, 100, 100, 0.3);
}

.corner-left, .corner-right {
  width: 15px;
  height: 15px;
  border: 2px solid rgba(255, 100, 100, 0.6);
}

.corner-left {
  border-right: none;
  border-bottom: none;
  border-top-left-radius: 4px;
}

.corner-right {
  border-left: none;
  border-bottom: none;
  border-top-right-radius: 4px;
}

.frame-bottom .corner-left {
  border-top: none;
  border-right: none;
  border-bottom-left-radius: 4px;
  border-top-left-radius: 0;
}

.frame-bottom .corner-right {
  border-top: none;
  border-left: none;
  border-bottom-right-radius: 4px;
  border-top-right-radius: 0;
}

.tech-line {
  flex: 1;
  height: 2px;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 100, 100, 0.8),
    rgba(255, 150, 100, 1),
    rgba(255, 100, 100, 0.8),
    transparent
  );
  margin: 0 5px;
  animation: techLinePulse 2s ease-in-out infinite alternate;
}

/* 弹窗内容 */
.dialog-content {
  position: relative;
  z-index: 10;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  text-align: center;
  gap: 20px;
}

/* 警告图标 */
.warning-icon {
  position: relative;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.warning-image {
  width: 60px;
  height: 60px;
  object-fit: contain;
  filter: drop-shadow(0 0 20px rgba(255, 100, 100, 0.8));
  animation: iconPulse 2s ease-in-out infinite;
  z-index: 2;
  position: relative;
}

.icon-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100px;
  height: 100px;
  transform: translate(-50%, -50%);
  background: radial-gradient(
    circle,
    rgba(255, 100, 100, 0.3),
    rgba(255, 100, 100, 0.1),
    transparent 70%
  );
  border-radius: 50%;
  animation: iconGlowPulse 2s ease-in-out infinite alternate;
}

/* 标题 */
.dialog-title {
  font-size: 28px;
  font-weight: 700;
  color: #ffffff;
  text-shadow: 0 0 20px rgba(255, 100, 100, 0.8);
  letter-spacing: 2px;
  margin: 0;
  animation: titleGlow 2s ease-in-out infinite alternate;
}

/* 内容文字 */
.dialog-message {
  font-size: 16px;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.9);
  text-shadow: 0 0 10px rgba(0, 150, 255, 0.4);
  line-height: 1.6;
  margin: 0;
  max-width: 320px;
}

/* 确认按钮 */
.confirm-button {
  position: relative;
  width: 120px;
  height: 45px;
  background: linear-gradient(
    145deg,
    rgba(150, 50, 50, 0.8),
    rgba(200, 80, 80, 0.9),
    rgba(150, 50, 50, 0.8)
  );
  border: 2px solid rgba(255, 100, 100, 0.6);
  border-radius: 6px;
  color: #ffffff;
  font-family: 'Orbitron', monospace;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
  backdrop-filter: blur(10px);
}

.button-text {
  position: relative;
  z-index: 2;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.button-glow {
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(
    45deg,
    rgba(255, 100, 100, 0.6),
    rgba(255, 150, 100, 0.8),
    rgba(255, 100, 100, 0.6)
  );
  border-radius: 8px;
  opacity: 0;
  transition: opacity 0.3s ease;
  filter: blur(4px);
}

.confirm-button:hover {
  background: linear-gradient(
    145deg,
    rgba(180, 70, 70, 0.9),
    rgba(220, 100, 100, 1),
    rgba(180, 70, 70, 0.9)
  );
  border-color: rgba(255, 100, 100, 0.8);
  box-shadow: 0 0 25px rgba(255, 100, 100, 0.6);
  transform: translateY(-2px);
}

.confirm-button:hover .button-glow {
  opacity: 1;
}

.confirm-button:active {
  transform: translateY(0);
}

/* 背景效果 */
.dialog-effects {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.bg-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 120%;
  height: 120%;
  transform: translate(-50%, -50%);
  background: radial-gradient(
    ellipse,
    rgba(255, 100, 100, 0.1),
    rgba(255, 100, 100, 0.05),
    transparent 70%
  );
  animation: bgPulse 3s ease-in-out infinite alternate;
}

.particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    radial-gradient(1px 1px at 80px 60px, rgba(255, 100, 100, 0.6), transparent),
    radial-gradient(1px 1px at 200px 120px, rgba(255, 255, 255, 0.3), transparent),
    radial-gradient(1px 1px at 300px 80px, rgba(255, 100, 100, 0.4), transparent),
    radial-gradient(1px 1px at 400px 200px, rgba(255, 255, 255, 0.2), transparent);
  background-repeat: no-repeat;
  animation: particleFloat 8s linear infinite;
}

/* 动画定义 */
@keyframes dialogSlideIn {
  0% {
    opacity: 0;
    transform: scale(0.8) translateY(-50px);
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

@keyframes techLinePulse {
  0% { opacity: 0.6; }
  100% { opacity: 1; }
}

@keyframes iconPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

@keyframes iconGlowPulse {
  0% { opacity: 0.3; transform: translate(-50%, -50%) scale(1); }
  100% { opacity: 0.6; transform: translate(-50%, -50%) scale(1.2); }
}

@keyframes titleGlow {
  0% { text-shadow: 0 0 20px rgba(255, 100, 100, 0.8); }
  100% { text-shadow: 0 0 30px rgba(255, 100, 100, 1), 0 0 50px rgba(255, 100, 100, 0.6); }
}

@keyframes bgPulse {
  0% { opacity: 0.3; }
  100% { opacity: 0.6; }
}

@keyframes particleFloat {
  0% { transform: translateY(0); }
  100% { transform: translateY(-20px); }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .access-denied-dialog {
    width: 90%;
    max-width: 400px;
    height: 280px;
  }
  
  .dialog-content {
    padding: 30px 20px;
    gap: 15px;
  }
  
  .warning-icon {
    width: 60px;
    height: 60px;
  }
  
  .warning-image {
    width: 45px;
    height: 45px;
  }
  
  .dialog-title {
    font-size: 24px;
  }
  
  .dialog-message {
    font-size: 14px;
    max-width: 280px;
  }
  
  .confirm-button {
    width: 100px;
    height: 40px;
    font-size: 12px;
  }
}
</style> 