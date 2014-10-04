SELECT u.seq_id,s.rank_1, s.rank_2, s.rank_3, s.rank_4  FROM snps as s, tag_index as t , unique_tags as u WHERE s.tag_id=t.id AND t.id=u.tag_id limit 0,30;
