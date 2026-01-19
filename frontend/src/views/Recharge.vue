<template>
  <div class="recharge-container">
    <h2>充值中心</h2>
    <div class="balance-info">
      <p>当前余额：<span class="balance">{{ userBalance }}</span> 书币</p>
    </div>
    
    <div class="recharge-options">
      <h3>选择充值金额</h3>
      <div class="amount-grid">
        <div 
          v-for="option in rechargeOptions" 
          :key="option.amount"
          :class="['amount-card', { selected: selectedAmount === option.amount }]"
          @click="selectAmount(option.amount)"
        >
          <div class="amount">{{ option.amount }}书币</div>
          <div class="price">￥{{ option.price }}</div>
          <div v-if="option.bonus" class="bonus">送{{ option.bonus }}书币</div>
        </div>
      </div>
    </div>

    <div class="payment-method">
      <h3>支付方式</h3>
      <div class="payment-options">
        <label class="payment-option">
          <input type="radio" v-model="paymentMethod" value="alipay" />
          <span>支付宝</span>
        </label>
        <label class="payment-option">
          <input type="radio" v-model="paymentMethod" value="wechat" />
          <span>微信支付</span>
        </label>
      </div>
    </div>

    <div class="recharge-summary">
      <div class="summary-item">
        <span>充值金额：</span>
        <span class="summary-value">{{ selectedAmount }}书币</span>
      </div>
      <div class="summary-item">
        <span>支付金额：</span>
        <span class="summary-value">￥{{ getSelectedPrice() }}</span>
      </div>
    </div>

    <button @click="recharge" class="recharge-btn" :disabled="!selectedAmount || !paymentMethod">
      立即充值
    </button>

    <div v-if="showSuccess" class="success-message">
      {{ successMsg }}
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userBalance: 0,
      selectedAmount: null,
      paymentMethod: '',
      showSuccess: false,
      successMsg: '',
      rechargeOptions: [
        { amount: 100, price: 10, bonus: 0 },
        { amount: 300, price: 25, bonus: 30 },
        { amount: 500, price: 40, bonus: 60 },
        { amount: 1000, price: 75, bonus: 150 },
        { amount: 2000, price: 140, bonus: 350 },
        { amount: 5000, price: 300, bonus: 1000 }
      ]
    }
  },
  mounted() {
    this.loadUserBalance()
  },
  methods: {
    async loadUserBalance() {
      try {
        const userObj = JSON.parse(localStorage.getItem('user') || '{}')
        const userId = userObj.id
        const res = await fetch(`/api/user/info/?user_id=${userId}`)
        const userInfo = await res.json()
        this.userBalance = userInfo.balance || 0
      } catch (e) {
        console.log('加载用户余额失败:', e)
      }
    },
    selectAmount(amount) {
      this.selectedAmount = amount
    },
    getSelectedPrice() {
      const option = this.rechargeOptions.find(opt => opt.amount === this.selectedAmount)
      return option ? option.price : 0
    },
    async recharge() {
      if (!this.selectedAmount || !this.paymentMethod) {
        alert('请选择充值金额和支付方式')
        return
      }
      try {
        const user = JSON.parse(localStorage.getItem('user') || '{}')
        const option = this.rechargeOptions.find(opt => opt.amount === this.selectedAmount)
        const bonus = option ? option.bonus : 0
        const res = await fetch('/api/recharge/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ user_id: user.id, amount: this.selectedAmount, bonus })
        })
        const data = await res.json()
        if (data.success) {
          this.showSuccess = true
          this.successMsg = '充值申请已提交，经过管理员审核后到账。'
          setTimeout(() => {
            this.showSuccess = false
            this.selectedAmount = null
            this.paymentMethod = ''
          }, 2000)
        } else {
          alert(data.msg || '充值失败')
        }
      } catch (e) {
        console.log('充值失败:', e)
      }
    }
  }
}
</script>

<style scoped>
.recharge-container {
  max-width: 600px;
  margin: 40px auto;
  background: #fffbe6;
  border-radius: 10px;
  box-shadow: 0 2px 12px #e0c97f;
  padding: 36px 32px 28px 32px;
  font-family: 'STKaiti', 'KaiTi', '楷体', 'serif';
}

.recharge-container h2 {
  font-size: 24px;
  color: #a67c00;
  margin-bottom: 24px;
  text-align: center;
}

.balance-info {
  background: #fdf6e3;
  border: 1px solid #e0c97f;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 24px;
  text-align: center;
}

.balance {
  font-size: 20px;
  color: #d4a017;
  font-weight: bold;
}

.recharge-options h3, .payment-method h3 {
  font-size: 18px;
  color: #a67c00;
  margin-bottom: 16px;
}

.amount-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 12px;
  margin-bottom: 24px;
}

.amount-card {
  background: #fdf6e3;
  border: 2px solid #e0c97f;
  border-radius: 8px;
  padding: 16px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
}

.amount-card:hover {
  border-color: #d4a017;
  background: #f5ecd7;
}

.amount-card.selected {
  border-color: #d4a017;
  background: #f5ecd7;
  box-shadow: 0 2px 8px #d4a017;
}

.amount {
  font-size: 16px;
  color: #a67c00;
  font-weight: bold;
  margin-bottom: 4px;
}

.price {
  font-size: 14px;
  color: #666;
  margin-bottom: 4px;
}

.bonus {
  font-size: 12px;
  color: #d4a017;
  background: #fdf6e3;
  border-radius: 4px;
  padding: 2px 6px;
}

.payment-options {
  display: flex;
  gap: 20px;
  margin-bottom: 24px;
}

.payment-option {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.payment-option input[type="radio"] {
  margin: 0;
}

.recharge-summary {
  background: #fdf6e3;
  border: 1px solid #e0c97f;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 24px;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.summary-item:last-child {
  margin-bottom: 0;
}

.summary-value {
  font-weight: bold;
  color: #d4a017;
}

.recharge-btn {
  width: 100%;
  background: #e6c97a;
  color: #5b4a1b;
  border: none;
  border-radius: 8px;
  padding: 12px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.2s;
}

.recharge-btn:hover:not(:disabled) {
  background: #f5e6b2;
}

.recharge-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.success-message {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
  border-radius: 8px;
  padding: 12px;
  text-align: center;
  margin-top: 16px;
}
</style> 