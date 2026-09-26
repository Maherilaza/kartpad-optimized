package dev.kartpad.android

import android.app.ActivityManager
import android.content.Context
import android.system.Os
import android.util.Log

internal object KartPadMemoryProfile {
    private const val CONSTRAINED_MEMORY_LIMIT_BYTES = 5L * 1024L * 1024L * 1024L

    fun configure(context: Context) {
        val manager = context.getSystemService(ActivityManager::class.java)
        val memoryInfo = ActivityManager.MemoryInfo()
        manager.getMemoryInfo(memoryInfo)
        val constrained = manager.isLowRamDevice ||
            memoryInfo.totalMem in 1L..CONSTRAINED_MEMORY_LIMIT_BYTES
        Os.setenv("KARTPAD_ANDROID_CONSTRAINED_MEMORY", if (constrained) "1" else "0", true)
        Log.i(
            TAG,
            "memoryProfile constrained=$constrained totalMiB=${memoryInfo.totalMem / (1024L * 1024L)}",
        )
    }

    private const val TAG = "KartPadMemoryProfile"
}
