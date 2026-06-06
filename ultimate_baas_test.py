import sys
import os
import asyncio
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.strategies.modes import MemoryStrategyManager, ModeType
from src.hardware_monitor.sensors import HardwareMonitor
from src.engine.predictive_engine import PredictiveHardwareEngine
from src.edge.offline_manager import EdgeOfflineManager

# Mock Donanım Durumu
mock_state = {
    "temp": 35.0,
    "cpu": 10.0,
    "battery": 100.0,
    "plugged": True
}

HardwareMonitor.get_temperature = lambda: mock_state["temp"]
HardwareMonitor.get_cpu_load = lambda: mock_state["cpu"]
HardwareMonitor.get_battery_info = lambda: {"percent": mock_state["battery"], "is_plugged": mock_state["plugged"]}

def mock_external_api(payload):
    """Bulut sistemine veri gönderen temsili dış API"""
    # Gerçekte burada requests.post() veya aiohttp olur
    pass

async def simulate_environmental_disaster():
    """Kayseri'de yaz sıcağında soğutma sistemlerinin çökme senaryosu"""
    print("\n[AŞAMA 1] Sistem stabil. Yankı sunucuları %10 yükle serin çalışıyor.")
    await asyncio.sleep(4)

    print("\n=======================================================")
    print("[AŞAMA 2] SOĞUTMA ARIZASI! Sunucu Isınmaya Başladı (Thermal Spike)")
    print("=======================================================")
    mock_state["cpu"] = 95.0
    for _ in range(5):
        mock_state["temp"] += 8.0 # Çok agresif ısı artışı!
        await asyncio.sleep(1)

    print("\n=======================================================")
    print("[AŞAMA 3] KRİZ ÇÖZÜLDÜ! Yedek Soğutma Devrede, Sistem Soğuyor")
    print("=======================================================")
    mock_state["cpu"] = 20.0
    mock_state["temp"] = 45.0
    await asyncio.sleep(6)


async def baas_middleware_simulator(request_id: int, strategy_manager: MemoryStrategyManager):
    """FastAPI Middleware'in sadeleştirilmiş simülasyonu"""
    if strategy_manager.current_mode == ModeType.ECO_THERMAL:
        # Sunucu yanıyor, Load Balancer'a 503 dönüp trafiği başka node'a yolla
        return 503, "Service Unavailable - Thermal Throttling Active"
    return 200, "OK - Request Processed"


async def ultimate_workload_test():
    strategy_manager = MemoryStrategyManager()
    edge_manager = EdgeOfflineManager(strategy_manager)
    engine = PredictiveHardwareEngine(strategy_manager, tick_rate=0.5, history_size=5)
    
    # Motoru ve Edge Arka Plan Senkronizasyon İşçisini başlat
    engine_task = asyncio.create_task(engine.start())
    sync_worker_task = asyncio.create_task(edge_manager.background_sync_worker())
    
    print("[TRAFİK] BaaS HTTP İstekleri ve Edge API Görevleri Başlıyor...\n")
    
    # 15 saniye boyunca sistemi test et
    for step in range(30): 
        # 1. Gelen BaaS Trafiği (FastAPI HTTP İstekleri)
        status, msg = await baas_middleware_simulator(step, strategy_manager)
        if status == 503 and step % 2 == 0:
            print(f"   [YANKI BaaS] Gelen İstek #{step} -> REDDEDİLDİ (503). Sunucu korunuyor.")
        elif status == 200 and step % 5 == 0:
            print(f"   [YANKI BaaS] Gelen İstek #{step} -> KABUL EDİLDİ (200).")

        # 2. Giden Edge Trafiği (Offline-First Koruması)
        # Sadece çift numaralı adımlarda dış API'ye veri göndermeye çalış
        if step % 2 == 0:
            payload = {"telemetry": "data", "id": step}
            result = await edge_manager.execute_or_queue_network_task(
                task_id=f"Task-{step}", 
                payload=payload, 
                external_api_call=mock_external_api
            )
            # Edge manager'ın kendi detaylı logları dışında ekstra log basmıyoruz, 
            # offline_manager.py içindeki print'ler durumu anlatacak.

        await asyncio.sleep(0.5)
        
    print("\n[FİNAL RAPORU] Ultimate Test Tamamlandı!")
    engine.stop()
    sync_worker_task.cancel() # Arka plan işçisini kapat
    await engine_task

async def main_run():
    disaster_task = asyncio.create_task(simulate_environmental_disaster())
    workload_task = asyncio.create_task(ultimate_workload_test())
    await asyncio.gather(disaster_task, workload_task)

if __name__ == "__main__":
    asyncio.run(main_run())