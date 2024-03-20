import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Veri setinizi yükleyin
df = pd.read_csv('/Users/nurkarakaya/graduationProject/graduationProject/Groceries_dataset.csv')

# Gerekli sütunları seçin
df = df[['Member_number', 'itemDescription']]

# Boş değerleri temizleyin
df.dropna(inplace=True)

# Kullanıcı-item matrisini oluşturun
user_item_matrix = df.groupby(['Member_number', 'itemDescription']).size().unstack().fillna(0)

# Index ve sütunları dizelere çevir
user_item_matrix.index = user_item_matrix.index.astype(str)
user_item_matrix.columns = user_item_matrix.columns.astype(str)

# Cosine Similarity'yi hesaplayın
cosine_sim = cosine_similarity(user_item_matrix)

# Matrisi DataFrame'e dönüştürün
cosine_sim_df = pd.DataFrame(cosine_sim, index=user_item_matrix.index, columns=user_item_matrix.index)

# Öneri fonksiyonu
def get_recommendations(member_id):
    member_id = str(member_id)  # member_id'yi string formata çevir

    if member_id not in user_item_matrix.index:
        print(f"Error: Member ID {member_id} not found in the dataset.")
        print("Veri setindeki kullanıcı numaraları:", user_item_matrix.index)
        return []

    similar_members = cosine_sim_df[member_id].sort_values(ascending=False).index[1:]
    recommendations = []

    for member in similar_members:
        similar_member_items = user_item_matrix.loc[member][user_item_matrix.loc[member] > 0].index
        user_items = user_item_matrix.loc[member_id][user_item_matrix.loc[member_id] > 0].index

        # Kullanıcının almadığı ürünleri öneri listesine ekle
        for item in similar_member_items:
            if item not in user_items:
                recommendations.append(item)

        # En çok satın alınan üç ürünü bul
        if len(recommendations) >= 3:
            break

    if not recommendations:
        print(f"No recommendations found for Member ID {member_id}.")
        return []

    print(f"Member ID {member_id} için önerilen ürünler:")
    for i, item in enumerate(recommendations, 1):
        print(f"{i}. {item}")

    return recommendations[:3]  # İlk 3 öneriyi al

# Kullanıcıdan member_id girişi alın
member_id_input = input("Lütfen Member ID girin: ")

# Kullanıcının girdiği member_id ile öneri fonksiyonunu çağırın
get_recommendations(member_id_input)
