import os
import shutil

# Konfigurasi class
class_map = {
    "helm": 0,
    "rompi": 1,
    "sarung_tangan": 2,
    "sepatu": 3
}

# Split dataset
splits = ["train", "valid", "test"]

# Path dasar input dan output
base_input = r"C:\Users\ACER\Videos\tes"
base_output = r"C:\Users\ACER\Videos\output"

# Buat struktur folder output
for split in splits:
    os.makedirs(os.path.join(base_output, split, "images"), exist_ok=True)
    os.makedirs(os.path.join(base_output, split, "labels"), exist_ok=True)

# Proses data dari setiap alat dan split
for alat, class_id in class_map.items():
    for split in splits:
        image_dir = os.path.join(base_input, alat, split, "images")
        label_dir = os.path.join(base_input, alat, split, "labels")

        if not os.path.exists(label_dir):
            print(f"[LEWAT] Folder label tidak ditemukan: {label_dir}")
            continue

        for label_file in os.listdir(label_dir):
            if not label_file.endswith(".txt"):
                continue

            label_path = os.path.join(label_dir, label_file)

            with open(label_path, "r") as f:
                lines = f.readlines()

            # Ubah class ID
            new_lines = []
            for line in lines:
                parts = line.strip().split()
                if len(parts) < 5:
                    continue
                parts[0] = str(class_id)
                new_lines.append(" ".join(parts))

            # Simpan label baru
            label_out_path = os.path.join(base_output, split, "labels", label_file)
            with open(label_out_path, "w") as f:
                f.write("\n".join(new_lines))

            # Copy image
            image_name = label_file.replace(".txt", ".jpg")  # Ubah jika perlu
            image_src_path = os.path.join(image_dir, image_name)
            image_dst_path = os.path.join(base_output, split, "images", image_name)

            if os.path.exists(image_src_path):
                shutil.copy(image_src_path, image_dst_path)
            else:
                print(f"[GAGAL COPY] Gambar tidak ditemukan: {image_src_path}")
