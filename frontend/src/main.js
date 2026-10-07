import { createApp } from 'vue'
import App from './App.vue'
import router from './routers/router.js'

// Design system styles (order matters: tokens first, then base)
import '@/styles/tokens.css'
import '@/styles/base.css'

// Global UI components
import AppButton from '@/components/ui/Button.vue'
import AppCard from '@/components/ui/Card.vue'
import AppInput from '@/components/ui/Input.vue'
import AppBadge from '@/components/ui/Badge.vue'
import AppModal from '@/components/ui/Modal.vue'
import AppSpinner from '@/components/ui/Spinner.vue'
import AppEmptyState from '@/components/ui/EmptyState.vue'
import AppLoadingState from '@/components/ui/LoadingState.vue'
import AppToastHost from '@/components/feedback/ToastHost.vue'
import ParkingLotCard from '@/components/ui/ParkingLotCard.vue'
import ActiveSessionCard from '@/components/ui/ActiveSessionCard.vue'
import KpiCard from '@/components/ui/KpiCard.vue'
import ParkingGrid from '@/components/ui/ParkingGrid.vue'

// Layout components
import AppShell from '@/components/layout/AppShell.vue'
import AppPageHeader from '@/components/layout/PageHeader.vue'

// Icons
import * as Icons from '@/components/icons'

const app = createApp(App)

app.use(router)

// Register global UI components
app.component('AppButton', AppButton)
app.component('AppCard', AppCard)
app.component('AppInput', AppInput)
app.component('AppBadge', AppBadge)
app.component('AppModal', AppModal)
app.component('AppSpinner', AppSpinner)
app.component('AppEmptyState', AppEmptyState)
app.component('AppLoadingState', AppLoadingState)
app.component('AppToastHost', AppToastHost)
app.component('ParkingLotCard', ParkingLotCard)
app.component('ActiveSessionCard', ActiveSessionCard)
app.component('KpiCard', KpiCard)
app.component('ParkingGrid', ParkingGrid)

// Register layout components
app.component('AppShell', AppShell)
app.component('AppPageHeader', AppPageHeader)

// Register all icons globally
Object.entries(Icons).forEach(([name, iconComponent]) => {
  app.component(name, iconComponent)
})

app.mount('#app')