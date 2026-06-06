import sys
import os
import asyncio

# Ana dizini yola ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.strategies.modes import MemoryStrategyManager
from src.memory_manager.allocator import MemoryFactory
from src.hardware_monitor.sensors import HardwareMonitor
from src.engine.predictive_engine import PredictiveHardwareEngine
from src.jit.bridge import JITRuntimeBridge

# Mock (Sahte) Donanım Durumu
mock_state = {
    "temp": 40.0,
    "cpu": 10.0,
    "battery": 100.0,
    "plugged": True
}

# Sensör okumalarını sahte durum objemize bağlıyoruz
HardwareMonitor.get_temperature = lambda: mock_state["temp"]
HardwareMonitor.get_cpu_load = lambda: mock_state["cpu"]
HardwareMonitor.get_battery_info = lambda: {"percent": mock_state["battery"], "is_plugged": mock_state["plugged"]}

async def simulate_hardware_meltdown():
    print("\n[SİMÜLASYON: AŞAMA 1] Sistem Serin (40°C), Şarja Takılı, Yük Hafif.")
    await asyncio.sleep(4)

    print("\n=======================================================")
    print("[SİMÜLASYON: AŞAMA 2] Isı Kademeli Artıyor! (Proaktif Analiz Başlıyor)")
    print("=======================================================")
    mock_state["cpu"] = 90.0
    
    # Her saniye sıcaklık 3 derece artıyor.
    # Proaktif Motor 15s sonrasını tahmin ettiği için (3 * 15 = 45 derece ileri!), 
    # gerçek sıcaklık henüz 50'lerdeyken sistemin 70'i geçeceğini öngörüp alarm verecek!
    for _ in range(8):
        mock_state["temp"] += 3.0
        await asyncio.sleep(1)

    print("\n=======================================================")
    print("[SİMÜLASYON: AŞAMA 3] Şarj Çekildi, Gerçek Sıcaklık 78°C'ye vuruyor!")
    print("=======================================================")
    mock_state["battery"] = 15.0
    mock_state["plugged"] = False
    mock_state["temp"] = 78.0
    await asyncio.sleep(5)


async def run_stress_test():
    strategy_manager = MemoryStrategyManager()
    
    # Başlangıçta havuzda 1000 obje yaratalım
    strategy_manager.object_pool._pool = [{"_id": i} for i in range(1000)]
    strategy_manager.object_pool._available = list(range(1000))
    
    memory_factory = MemoryFactory(strategy_manager)
    jit_bridge = JITRuntimeBridge(strategy_manager)
    
    # Yeni Proaktif Motoru başlatıyoruz (hızlı tepki için history_size=5 saniye)
    engine = PredictiveHardwareEngine(strategy_manager, tick_rate=1.0, history_size=5)
    
    # JIT Köprüsü Entegrasyonu: Ağır işlem yapan bir fonksiyonu sarmalıyoruz
    @jit_bridge.hardware_jit_optimizer(loop_identifier="Kardelen_Agir_Dongu", safe_fallback_value={"data": "GUVENLI_CACHE_VERISI"})
    def run_heavy_computation(step_id):
        # Normalde işlemciyi çok yoracak bir yapay zeka veya yorumlayıcı (interpreter) döngüsü
        return {"data": f"Gercek_Hesaplama_{step_id}"}

    async def brutal_memory_workload():
        print("[İŞ YÜKÜ] Acımasız bellek tahsis ve JIT testleri başlatıldı...\n")
        allocated = []
        
        for step in range(150): 
            # 1. JIT KÖPRÜSÜ TESTİ: Arada bir ağır hesaplama fonksiyonunu çağır
            if step % 15 == 0:
                result = run_heavy_computation(step)
                print(f"   [APP JIT ÇIKTISI] Adım {step} -> {result}")

            # 2. BELLEK YÖNETİMİ TESTİ (Allocation)
            for _ in range(100): 
                try:
                    obj, pool_id = memory_factory.allocate()
                    obj["payload"] = "Heavy Payload String"
                    allocated.append((obj, pool_id))
                except MemoryError as e:
                    if step % 10 == 0: 
                        print(f"   [APP UYARISI] {e}")
                    break
            
            free_count = 50 if memory_factory.current_active_mode != "Eco/Thermal" else 80
            for _ in range(min(free_count, len(allocated))):
                obj, pool_id = allocated.pop(0)
                memory_factory.free(obj, pool_id)
                
            await asyncio.sleep(0.1)
            
        print(f"\n[İŞ YÜKÜ] Test tamamlandı. Kalan aktif nesne sayısı: {len(allocated)}")

    # Görevleri başlat
    engine_task = asyncio.create_task(engine.start())
    meltdown_task = asyncio.create_task(simulate_hardware_meltdown())
    workload_task = asyncio.create_task(brutal_memory_workload())
    
    await asyncio.gather(meltdown_task, workload_task)
    
    engine.stop()
    await engine_task

if __name__ == "__main__":
    asyncio.run(run_stress_test())