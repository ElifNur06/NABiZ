import sys
import os
import asyncio
import time

# Ana dizini yola ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.strategies.modes import MemoryStrategyManager
from src.memory_manager.allocator import MemoryFactory
from src.hardware_monitor.sensors import HardwareMonitor
from src.engine.predictive_engine import PredictiveHardwareEngine
from src.jit.bridge import JITRuntimeBridge

# Mock (Sahte) Donanım Durumu - Başlangıç
mock_state = {
    "temp": 45.0,
    "cpu": 15.0,
    "battery": 100.0,
    "plugged": True
}

HardwareMonitor.get_temperature = lambda: mock_state["temp"]
HardwareMonitor.get_cpu_load = lambda: mock_state["cpu"]
HardwareMonitor.get_battery_info = lambda: {"percent": mock_state["battery"], "is_plugged": mock_state["plugged"]}

async def simulate_thermal_runaway():
    """Donanımın saniyeler içinde felakete sürüklendiği 'Termal Kaçak' senaryosu"""
    print("\n[SİMÜLASYON: AŞAMA 1] Fırtına Öncesi Sessizlik (45°C)")
    await asyncio.sleep(3)

    print("\n=======================================================")
    print("[SİMÜLASYON: AŞAMA 2] DDOS/Kripto Saldırısı! CPU %100, Isı Patlaması!")
    print("=======================================================")
    mock_state["cpu"] = 100.0
    
    # Isı katlanarak (eksponansiyel) artıyor! Proaktif motorun bunu saniyesinde yakalaması lazım.
    for i in range(1, 6):
        mock_state["temp"] += (i * 4) # 4, 8, 12, 16 derece anlık zıplamalar
        await asyncio.sleep(1)

    print("\n=======================================================")
    print("[SİMÜLASYON: AŞAMA 3] GÜÇ KAYBI! Batarya Çakıldı, Sistem 90°C!")
    print("=======================================================")
    mock_state["plugged"] = False
    mock_state["battery"] = 5.0
    mock_state["temp"] = 90.0
    await asyncio.sleep(5)


async def impossible_doomsday_workload():
    strategy_manager = MemoryStrategyManager()
    
    # DİKKAT: Havuzda SADECE 500 obje var. Sistemi bilerek aç bırakıyoruz.
    strategy_manager.object_pool._pool = [{"_id": i} for i in range(500)]
    strategy_manager.object_pool._available = list(range(500))
    
    memory_factory = MemoryFactory(strategy_manager)
    jit_bridge = JITRuntimeBridge(strategy_manager)
    
    # Proaktif Motor (Çok agresif, 3 saniyelik geçmişe bakıp karar verecek)
    engine = PredictiveHardwareEngine(strategy_manager, tick_rate=0.5, history_size=6)
    
    @jit_bridge.hardware_jit_optimizer(loop_identifier="Olumcul_YapayZeka_Dongusu", safe_fallback_value={"status": "BYPASS_EDILDI", "risk": "CRITICAL"})
    def lethal_computation():
        # JIT köprüsü olmazsa sistemi kilitleyecek sahte ağır döngü
        time.sleep(0.01) 
        return {"status": "TAMAMLANDI", "risk": "YOK"}

    engine_task = asyncio.create_task(engine.start())
    
    print("[İŞ YÜKÜ] 'Bellek Bombası' devrede. Sistem yok edilmeye çalışılıyor...\n")
    allocated = []
    
    # 10 saniye boyunca sistemi durmaksızın bombala
    for step in range(100): 
        # 1. JIT SPAM TESTİ: Saniyede 10 kere ağır fonksiyonu çağır
        result = lethal_computation()
        if step % 10 == 0:
            print(f"   [APP JIT DURUMU] Adım {step} -> Çıktı: {result['status']}")

        # 2. BELLEK BOMBASI (Memory Bomb): Havuzda 500 yer varken, 2000 nesne talep et!
        if step == 40:
            print("\n   [!!! APP SALDIRISI !!!] Tek seferde 2000 nesne (Bellek Bombası) talep ediliyor!")
            bomb_failed_count = 0
            for _ in range(2000): 
                try:
                    obj, pool_id = memory_factory.allocate()
                    obj["payload"] = "FATAL_BOMB_PAYLOAD"
                    allocated.append((obj, pool_id))
                except MemoryError:
                    bomb_failed_count += 1
            print(f"   [SAVUNMA RAPORU] Bellek Bombası absorbe edildi! {bomb_failed_count} istek donanımı korumak için REDDEDİLDİ!\n")

        # Standart tahsisat
        for _ in range(10): 
            try:
                obj, pool_id = memory_factory.allocate()
                allocated.append((obj, pool_id))
            except MemoryError:
                pass # Sessizce yut
        
        # Temizlik (Sadece Eco modda agresif temizlik yap, yoksa bellek şişsin)
        free_count = 5 if memory_factory.current_active_mode != "Eco/Thermal" else 50
        for _ in range(min(free_count, len(allocated))):
            obj, pool_id = allocated.pop(0)
            memory_factory.free(obj, pool_id)
            
        await asyncio.sleep(0.1)
        
    print(f"\n[KIYAMET TESTİ SONUCU] Sistem hayatta kaldı! Çökme: YOK. Kalan Nesne: {len(allocated)}")
    engine.stop()
    await engine_task

async def main_run():
    meltdown_task = asyncio.create_task(simulate_thermal_runaway())
    workload_task = asyncio.create_task(impossible_doomsday_workload())
    await asyncio.gather(meltdown_task, workload_task)

if __name__ == "__main__":
    asyncio.run(main_run())