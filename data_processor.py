import json
import os

def process_traceroute_file(file_path):
    # Define o caminho de saída adicionando "_essential" ao nome do arquivo original
    output_path = os.path.splitext(file_path)[0] + "_essential.json"

    # Extrai os campos necessários: "dst_name", "timestamp", último "hop" e "prb_id"
    extracted_data = []

    with open(file_path, 'r') as f:
        for line in f:
            traceroute = json.loads(line)
            dst_name = traceroute.get("dst_name")
            timestamp = traceroute.get("timestamp")
            prb_id = traceroute.get("prb_id")
            
            # Obtem o último hop e o número do hop
            result_hops = traceroute.get("result", [])
            if result_hops:
                last_hop_info = result_hops[-1]
                hop_number = last_hop_info.get("hop")
                
                #Filtra todas as entradas "result" que não possuem "rtt"
                rtt_values = [hop.get("rtt") for hop in last_hop_info.get("result", []) if hop.get("rtt") is not None]
                
                avg_rtt = sum(rtt_values) / len(rtt_values) if rtt_values else None
                last_hop = last_hop_info.get("result")[-1].get("from", "*") if last_hop_info.get("result") else "*"
            else:
                hop_number = None
                avg_rtt = None
                last_hop = "*"
            
            extracted_data.append({
                "dst_name": dst_name,
                "timestamp": timestamp,
                "last_hop": last_hop,
                "hop_number": hop_number,
                "avg_rtt": avg_rtt,
                "prb_id": prb_id
            })

    # Salva os dados extraídos em um novo arquivo JSON
    with open(output_path, 'w') as f:
        json.dump(extracted_data, f, indent=4)

    return output_path

file_name = input("Digite o nome do arquivo JSON (incluindo .json): ")
output_file = process_traceroute_file(file_name)
print(f"Essential data saved to: {output_file}")
