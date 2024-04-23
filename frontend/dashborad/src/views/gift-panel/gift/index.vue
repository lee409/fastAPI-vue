<template>
  <div class="app-container">
    <el-form ref="queryForm" :model="queryParams" :inline="true" label-width="68px">
      <el-form-item label="编号" prop="id">
        <el-input
          v-model="queryParams.gift_num"
          placeholder="请输入礼物id"
          clearable
          size="small"
          style="width: 200px"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="礼物名称" prop="nickname">
        <el-input
          v-model="queryParams.gift_name"
          placeholder="请输入礼物名称"
          clearable
          size="small"
          style="width: 200px"
          @keyup.enter.native="handleQuery"
        />
      </el-form-item>
      <el-form-item label="状态" prop="status">
        <el-select v-model="queryParams.enableflag" placeholder="礼物状态" clearable size="small" style="width: 200px">
          <el-option v-for="dict in statusOptions" :key="dict.id" :label="dict.label" :value="dict.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="创建时间">
        <el-date-picker
          v-model="dateRange"
          size="small"
          style="width: 240px"
          value-format="yyyy-MM-dd"
          type="daterange"
          range-separator="~"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="mini" @click="handleQuery">搜索</el-button>
        <el-button icon="el-icon-refresh" size="mini" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button type="primary" icon="el-icon-plus" size="mini" @click="handleAdd">新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="success" icon="el-icon-edit" size="mini" :disabled="single" @click="handleUpdate">修改
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          icon="el-icon-delete"
          size="mini"
          :disabled="multiple"
          @click="handleDelete"
        >删除
        </el-button>
      </el-col>
    </el-row>

    <el-table v-loading="loading" :data="userList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="50" align="center" />
      <el-table-column label="编号" align="center" prop="gift_num" width="85" :show-overflow-tooltip="true" />
      <el-table-column label="礼物名称" align="center" prop="gift_name" :show-overflow-tooltip="true" />
      <el-table-column label="状态" align="center" prop="status" width="70" :formatter="statusFormat" />
      <el-table-column label="创建时间" align="center" prop="created_ts">
        <template slot-scope="scope">
          <span>{{ parseTime(scope.row.created_ts) }}</span>
        </template>
      </el-table-column>
      <!--      <el-table-column label="更新时间" align="center" prop="modified_ts">-->
      <!--        <template slot-scope="scope">-->
      <!--          <span>{{ parseTime(scope.row.modified_ts) }}</span>-->
      <!--        </template>-->
      <!--      </el-table-column>-->
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button size="mini" type="text" icon="el-icon-edit" @click="handleUpdate(scope.row)">修改</el-button>
          <el-button size="mini" type="text" icon="el-icon-delete" @click="handleDelete(scope.row)">删除</el-button>
          <el-button size="mini" type="text" icon="el-icon-key" @click="handleResetPwd(scope.row)">重置</el-button>
        </template>
      </el-table-column>
    </el-table>
    <pagination
      v-show="total>0"
      :total="total"
      :page.sync="queryParams.page"
      :limit.sync="queryParams.limit"
      @pagination="getList"
    />

    <!-- 添加或修改参数配置对话框 -->
    <el-dialog :title="title" :visible.sync="open" width="600px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-row>
          <el-col :span="12">
            <el-form-item label="用户昵称" prop="nickname">
              <el-input v-model="form.nickname" placeholder="请输入用户昵称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="用户名" prop="username">
              <el-input v-model="form.username" placeholder="请输入用户名" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="手机号码" prop="phone">
              <el-input v-model="form.phone" placeholder="请输入手机号码" maxlength="11" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="form.email" placeholder="请输入邮箱" maxlength="18" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="用户性别" prop="sex">
              <el-select v-model="form.sex" placeholder="请选择">
                <el-option v-for="dict in sexOptions" :key="dict.value" :label="dict.label" :value="dict.value" />
              </el-select>
            </el-form-item>
          </el-col>

          <el-col :span="12">
            <el-form-item label="状态" prop="status">
              <el-select v-model="form.status" placeholder="请选择">
                <el-option v-for="item in statusOptions" :key="item.value" :label="item.label" :value="item.value" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="用户头像" prop="avatar">
              <avatar-upload v-if="open" :avatar="fileBase + form.avatar" @uploadAvatar="uploadPicture" />
              <span class="upload-img-tip">提示：点击图片可进行裁剪和上传</span>
              <el-upload
                class="avatar-uploader"
                :headers="headers"
                :action="uploadAvatarUrl"
                accept=".jpg,.png,.ico,.gif,.jpeg,.tiff"
                :show-file-list="false"
                :on-success="handleAvatarSuccess"
                :on-error="handleAvatarError"
                :before-upload="beforeAvatarUpload"
                name="img"
                size="mini"
              >
                <el-button type="primary" size="mini">上传</el-button>
                <el-button type="success" size="mini" @click.stop="handleDefaultImg">默认</el-button>
              </el-upload>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="角色" prop="roles">
              <el-select v-model="form.roles" multiple placeholder="请选择">
                <el-option v-for="item in roleOptions" :key="item.id" :label="item.name" :value="item.id">
                  <span style="float: left">{{ item.name }}</span>
                  <span style="float: right; color: #8492a6; font-size: 13px; margin-right: 15px;">{{ item.key }}</span>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>
import {
  // eslint-disable-next-line no-unused-vars
  listGift
} from '@/api/gift/gift'
import { getToken } from '@/utils/auth'

export default {
  name: 'GiftPanel',
  data() {
    return {
      // 遮罩层
      loading: true,
      // 选中数组
      ids: [],
      // 非单个禁用
      single: true,
      // 非多个禁用
      multiple: true,
      // 总条数
      total: 0,
      // 用户表格数据
      userList: null,
      // 弹出层标题
      title: '',

      // 是否显示弹出层
      open: false,
      // 部门名称
      deptName: undefined,
      // 日期范围
      dateRange: [],
      // 状态数据字典
      statusOptions: [], defaultStatusValue: undefined,
      // 性别状态字典
      sexOptions: [], defaultSexValue: undefined,
      // 角色选项
      roleOptions: [], defaultRolesId: [],
      // 表单参数
      form: {},
      defaultProps: {
        children: 'children',
        label: 'name'
      },
      // 查询参数
      queryParams: {
        page: 1,
        limit: 20,
        gift_num: undefined,
        gift_name: undefined,
        enableflag: undefined,
        created_after_ts: undefined,
        created_before_ts: undefined
      },
      // 头像
      fileBase: process.env.VUE_APP_MEDIA_BASE,
      defaultAvatar: 'images/avatar/default/avatar.jpg',
      // 设置上传的请求头部
      headers: { Authorization: 'Token ' + getToken() },
      // 上传网站图片地址
      uploadAvatarUrl: process.env.VUE_APP_BASE_API + 'permission/user/profile/avatar',
      // 表单校验
      rules: {}
    }
  },
  created() {
    this.getList()
  },
  methods: {
    // Your gift panel methods here
    getList() {
      this.loading = true
      console.log(this.dateRange)
      if (this.dateRange.length > 0) {
        this.queryParams.created_after_ts = parseInt((new Date(this.dateRange[0] + ' 00:00:00')).getTime() / 1000)
        this.queryParams.created_before_ts = parseInt((new Date(this.dateRange[1] + ' 23:59:59')).getTime() / 1000)
      }
      console.log(this.queryParams)
      listGift(this.queryParams).then(response => {
        this.userList = response.data.results
        this.total = response.data.total
        this.loading = false
      })
    }

  }
}
</script>

<style scoped>
.gift-panel {
  /* Your gift panel styles here */
}
</style>
