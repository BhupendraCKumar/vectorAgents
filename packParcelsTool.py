from py3dbp import Packer, Bin, Item
# from langchain_core.tools import tool
from supportUDFs import CustomerSupportState
import pandas as pd
import json
from decimal import Decimal, InvalidOperation
# @tool
def container_packing(state:CustomerSupportState):
    packer = Packer()
    # organize_parcels()
    container = Bin(
        name="MainContainer",
        width=50,
        height=50,
        depth=50,
        max_weight=float('inf')
    )

    packer.add_bin(container)
    state['organized_parcels'] = organize_parcels(state['file_path'],state['tsp_route'])
    # Iterate over parcels sorted by optimized route
    for idx, row in state['organized_parcels'].iterrows():
        item = Item(
            name=f"Parcel-{idx}",
            width=row['width'],
            height=row['height'],
            depth=row['length'],
            weight=1  # Assume weight=1 for now, adjust if needed
        )
        packer.add_item(item)
    
    try:
        packer.pack(
            bigger_first=True,
            distribute_items=False,
            # fix_point=True,
            number_of_decimals=0
        )
    except InvalidOperation as e:
        print(f"Invalid operation: {e}")

    summary = []

    for bin in packer.bins:
        bin_info = {
            "bin_name": bin.name,
            "bin_dimensions": f"{bin.width}x{bin.height}x{bin.depth}",
            "packed_items": [],
        }

        for i, item in enumerate(bin.items):
            bin_info["packed_items"].append({
                "sequence": i + 1,
                "item_name": item.name,
                "dimensions": f"{item.width}x{item.height}x{item.depth}",
                "position": f"{item.position}",
            })

        summary.append(bin_info)
    state['packing_summary'] = json.dumps(summary,indent=2)

    return state
    

def organize_parcels(file_path,route):
    # Reorder based on the TSP route
    df = pd.read_csv(file_path)
    # route = state['tsp_route']
    organized = df.iloc[route].reset_index(drop=True)
    # state['organized_parcels'] = organized
    return organized