<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">视频创意管理</div>
        <div class="page-subtitle">上传视频 · 查看审核状态 · 管理投放创意</div>
      </div>
    </div>

    <!-- Step 1: 选择 Campaign -->
    <div class="card" style="margin-bottom:16px">
      <div style="font-weight:600;margin-bottom:12px">1. 选择 Campaign</div>
      <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
        <select v-model="selectedAdv" @change="loadCampaigns" style="width:200px">
          <option value="">选择广告账户</option>
          <option v-for="a in advertisers" :key="a.advertiser_id" :value="a.advertiser_id">
            {{ a.name || a.advertiser_id }}
          </option>
        </select>
        <select v-model="selectedCampaign" style="width:240px">
          <option value="">选择推广计划</option>
          <option v-for="c in campaigns" :key="c.campaign_id" :value="c.campaign_id">
            {{ c.campaign_name || c.campaign_id }}
          </option>
        </select>
      </div>
    </div>

    <!-- Step 2: 上传视频 -->
    <div class="card" style="margin-bottom:16px">
      <div style="font-weight:600;margin-bottom:12px">2. 上传视频素材</div>
      <div style="display:flex;gap:12px;align-items:flex-start;flex-wrap:wrap">
        <div class="upload-area" @click="$refs.fileInput.click()" @dragover.prevent @drop.prevent="onDrop">
          <div style="font-size:32px;opacity:0.4">📤</div>
          <div style="font-size:13px;color:var(--text-muted);margin-top:4px">点击或拖拽视频文件</div>
          <div style="font-size:11px;color:var(--text-muted)">支持 MP4，最大 500MB</div>
          <input ref="fileInput" type="file" accept="video/*" multiple hidden @change="onFilesSelect" />
        </div>
        <!-- 上传队列 -->
        <div v-if="uploadQueue.length" style="flex:1;min-width:300px">
          <div v-for="(f, idx) in uploadQueue" :key="idx" class="upload-item">
            <div style="display:flex;justify-content:space-between;align-items:center">
              <div style="font-size:13px;font-weight:500;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:250px">
                {{ f.file.name }}
              </div>
              <div style="font-size:11px;color:var(--text-muted)">{{ (f.file.size / 1024 / 1024).toFixed(1) }}MB</div>
            </div>
            <div v-if="f.status === 'uploading'" class="progress-bar">
              <div class="progress-fill" :style="{width: f.progress + '%'}"></div>
            </div>
            <div v-if="f.status === 'done'" style="font-size:11px;color:var(--success)">
              上传成功 · video_id: {{ f.videoId }}
            </div>
            <div v-if="f.status === 'error'" style="font-size:11px;color:var(--danger)">
              {{ f.error }}
            </div>
            <div v-if="f.status === 'pending'" style="font-size:11px;color:var(--text-muted)">等待上传</div>
          </div>
          <button v-if="uploadQueue.some(f => f.status === 'pending')" class="btn btn-primary" style="margin-top:8px"
            :disabled="uploading" @click="startUpload">
            {{ uploading ? '上传中...' : '开始上传' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Step 3: 创意列表 -->
    <div class="card">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
        <div style="font-weight:600">3. 投放中的创意</div>
        <button class="btn btn-ghost" style="padding:3px 10px;font-size:12px" @click="loadPosts" :disabled="!selectedAdv">
          刷新
        </button>
      </div>
      <div v-if="postsLoading" style="padding:30px;text-align:center;color:var(--text-muted)">加载中...</div>
      <div v-else-if="!posts.length" class="empty-state">
        <div class="empty-icon">🎬</div>
        <div>{{ selectedAdv ? '暂无创意数据' : '请先选择广告账户' }}</div>
      </div>
      <div v-else class="post-grid">
        <div v-for="p in posts" :key="p.item_id" class="post-card" :class="{'post-excluded': p._excluded}">
          <div class="post-thumb">
            <img v-if="p.thumbnail_url || p.image_url" :src="p.thumbnail_url || p.image_url"
                 @error="$event.target.style.display='none'" />
            <div v-else style="display:flex;align-items:center;justify-content:center;height:100%;font-size:24px;opacity:0.3">🎬</div>
          </div>
          <div class="post-info">
            <div class="post-title" :title="p.title || p.product_name">{{ p.title || p.product_name || '创意 #' + (p.item_id||'').slice(-6) }}</div>
            <div style="font-size:11px;color:var(--text-muted)">
              <span v-if="p.author">@{{ p.author }}</span>
              <span v-if="p.total_spend"> · ${{ Number(p.total_spend||0).toFixed(2) }}</span>
              <span v-if="p.total_orders"> · {{ p.total_orders }}单</span>
            </div>
            <div style="display:flex;gap:4px;margin-top:6px">
              <a v-if="p.tiktok_url" :href="p.tiktok_url" target="_blank" class="btn btn-ghost" style="padding:2px 8px;font-size:11px">▶ 观看</a>
              <button v-if="!p._excluded" class="btn btn-ghost" style="padding:2px 8px;font-size:11px;color:var(--danger)"
                @click="excludePost(p)">🚫 排除</button>
              <button v-else class="btn btn-ghost" style="padding:2px 8px;font-size:11px;color:var(--success)"
                @click="restorePost(p)">✅ 恢复</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { api, advertiserApi } from '../api'

const advertisers = ref([])
const campaigns = ref([])
const selectedAdv = ref('')
const selectedCampaign = ref('')

// 上传
const uploadQueue = ref([])
const uploading = ref(false)

// 创意列表
const posts = ref([])
const postsLoading = ref(false)

onMounted(async () => {
  try {
    const data = await advertiserApi.list()
    advertisers.value = data.advertisers || []
    if (advertisers.value.length === 1) {
      selectedAdv.value = advertisers.value[0].advertiser_id
      await loadCampaigns()
      await loadPosts()
    }
  } catch {}
})

async function loadCampaigns() {
  campaigns.value = []
  selectedCampaign.value = ''
  if (!selectedAdv.value) return
  try {
    const data = await api.get('/gmvmax/campaigns', { params: { advertiser_id: selectedAdv.value } })
    campaigns.value = data.campaigns || data.items || []
  } catch {}
  await loadPosts()
}

watch(selectedCampaign, loadPosts)

async function loadPosts() {
  if (!selectedAdv.value) return
  postsLoading.value = true
  try {
    const params = { advertiser_id: selectedAdv.value }
    if (selectedCampaign.value) params.campaign_id = selectedCampaign.value
    const data = await api.get('/gmvmax/creative/posts', { params })
    posts.value = (data.posts || []).map(p => ({ ...p, _excluded: false }))
  } catch (e) {
    console.error('Load posts failed', e)
    posts.value = []
  } finally {
    postsLoading.value = false
  }
}

// 上传
function onFilesSelect(e) {
  addFiles(Array.from(e.target.files))
  e.target.value = ''
}
function onDrop(e) {
  addFiles(Array.from(e.dataTransfer.files).filter(f => f.type.startsWith('video/')))
}
function addFiles(files) {
  for (const file of files) {
    uploadQueue.value.push({ file, status: 'pending', progress: 0, videoId: '', error: '' })
  }
}

async function startUpload() {
  if (!selectedAdv.value) { alert('请先选择广告账户'); return }
  uploading.value = true
  for (const item of uploadQueue.value) {
    if (item.status !== 'pending') continue
    item.status = 'uploading'
    try {
      const formData = new FormData()
      formData.append('advertiser_id', selectedAdv.value)
      formData.append('file', item.file)
      formData.append('video_name', item.file.name.replace(/\.[^.]+$/, ''))
      const res = await api.post('/ads/video/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 300000,
        onUploadProgress: e => {
          if (e.total) item.progress = Math.round(e.loaded / e.total * 100)
        },
      })
      item.videoId = res.video_id || res.data?.video_id || ''
      item.status = 'done'
    } catch (e) {
      item.status = 'error'
      const detail = e.response?.data?.detail
      item.error = Array.isArray(detail)
        ? detail.map(d => d.msg || JSON.stringify(d)).join('; ')
        : (detail || e.message)
    }
  }
  uploading.value = false
}

// 排除/恢复创意
async function excludePost(p) {
  if (!selectedCampaign.value) { alert('请先选择 Campaign'); return }
  try {
    await api.post('/gmvmax/creative/manage', {
      advertiser_id: selectedAdv.value,
      campaign_id: selectedCampaign.value,
      action: 'REMOVE',
      item_ids: [p.item_id],
    })
    p._excluded = true
  } catch (e) {
    alert('排除失败: ' + (e.response?.data?.detail || e.message))
  }
}

async function restorePost(p) {
  if (!selectedCampaign.value) { alert('请先选择 Campaign'); return }
  try {
    await api.post('/gmvmax/creative/manage', {
      advertiser_id: selectedAdv.value,
      campaign_id: selectedCampaign.value,
      action: 'RESTORE',
      item_ids: [p.item_id],
    })
    p._excluded = false
  } catch (e) {
    alert('恢复失败: ' + (e.response?.data?.detail || e.message))
  }
}
</script>

<style scoped>
.upload-area {
  width: 200px; height: 140px;
  border: 2px dashed var(--border); border-radius: 12px;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  cursor: pointer; transition: all 0.2s;
}
.upload-area:hover { border-color: var(--primary); background: rgba(99,102,241,0.04); }

.upload-item {
  padding: 8px 12px; border: 1px solid var(--border); border-radius: 8px;
  margin-bottom: 6px; background: var(--bg);
}
.progress-bar {
  height: 4px; background: var(--bg-hover); border-radius: 2px; margin-top: 6px; overflow: hidden;
}
.progress-fill {
  height: 100%; background: var(--primary); transition: width 0.3s;
}

.post-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 12px;
}
.post-card {
  display: flex; gap: 10px; padding: 10px; border: 1px solid var(--border);
  border-radius: 8px; background: var(--bg); transition: all 0.15s;
}
.post-card:hover { border-color: var(--primary); }
.post-card.post-excluded { opacity: 0.5; border-color: var(--danger); }
.post-thumb {
  width: 80px; height: 100px; flex-shrink: 0; border-radius: 6px; overflow: hidden;
  background: var(--bg-hover);
}
.post-thumb img { width: 100%; height: 100%; object-fit: cover; }
.post-info { flex: 1; min-width: 0; }
.post-title {
  font-size: 13px; font-weight: 500; line-height: 1.4;
  overflow: hidden; text-overflow: ellipsis;
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;
}

.empty-state { text-align: center; padding: 40px; color: var(--text-muted); }
.empty-icon { font-size: 36px; margin-bottom: 8px; }
</style>
