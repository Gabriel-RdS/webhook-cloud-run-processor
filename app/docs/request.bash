curl --location --request POST 'https://unification.useinsider.com/api/raw/v1/export' \
--header 'X-PARTNER-NAME: ayabooksexatecnologia' \
--header 'X-REQUEST-TOKEN: 1a2b3c4d5e6f' \
--header 'Content-Type: application/json' \
--data-raw '{
   "segment": {
        "segment_id": 123456789
    },
   "attributes":[
      "*"
   ],
   "events":{
      "start_date":1606311893,
      "end_date":1611582293,
      "wanted":[
         {"event_name":"af_login", "params":["custom", "timestamp"]},
         {"event_name":"af_search", "params":["custom", "timestamp"]},
         {"event_name":"af_share", "params":["custom", "timestamp"]},
         {"event_name":"alterar_email", "params":["custom", "timestamp"]},
         {"event_name":"alterar_senha", "params":["custom", "timestamp"]},
         {"event_name":"assine_agora", "params":["custom", "timestamp"]},
         {"event_name":"best_seller_exchange", "params":["custom", "timestamp"]},
         {"event_name":"cart_clearance", "params":["default", "timestamp"]},
         {"event_name":"cart_page_view", "params":["default", "timestamp"]},
         {"event_name":"completar_cadastro", "params":["custom", "timestamp"]},
         {"event_name":"purchase", "params":["default", "timestamp"]},
         {"event_name":"content_end", "params":["custom", "timestamp"]},
         {"event_name":"content_favorite", "params":["custom", "timestamp"]},
         {"event_name":"content_in_progress", "params":["custom", "timestamp"]},
         {"event_name":"content_open", "params":["custom", "timestamp"]},
         {"event_name":"criar_conta_check_email", "params":["custom", "timestamp"]},
         {"event_name":"criar_conta_continuar_depois", "params":["custom", "timestamp"]},
         {"event_name":"criar_conta_finalizar", "params":["custom", "timestamp"]},
         {"event_name":"crie_sua_conta_pin", "params":["custom", "timestamp"]},
         {"event_name":"delete_account", "params":["custom", "timestamp"]},
         {"event_name":"editar_perfil", "params":["custom", "timestamp"]},
         {"event_name":"email_blocked", "params":["default", "timestamp"]},
         {"event_name":"email_bounce", "params":["default", "timestamp"]},
         {"event_name":"email_click", "params":["default", "timestamp"]},
         {"event_name":"email_delivered", "params":["default", "timestamp"]},
         {"event_name":"email_drop", "params":["default", "timestamp"]},
         {"event_name":"email_invalid", "params":["default", "timestamp"]},
         {"event_name":"email_open", "params":["default", "timestamp"]},
         {"event_name":"email_resubscribe", "params":["default", "timestamp"]},
         {"event_name":"email_spam_report", "params":["default", "timestamp"]},
         {"event_name":"email_systemdrop", "params":["custom", "timestamp"]},
         {"event_name":"email_unsubscribe", "params":["default", "timestamp"]},
         {"event_name":"esqueci_email", "params":["custom", "timestamp"]},
         {"event_name":"filtro_estante_categorias", "params":["custom", "timestamp"]},
         {"event_name":"geofence_trigger", "params":["default", "timestamp"]},
         {"event_name":"homepage_view", "params":["default", "timestamp"]},
         {"event_name":"inapp_view", "params":["default", "timestamp"]},
         {"event_name":"social_proof_view", "params":["default", "timestamp"]},
         {"event_name":"interest", "params":["custom", "timestamp"]},
         {"event_name":"add_to_cart", "params":["default", "timestamp"]},
         {"event_name":"remove_from_cart", "params":["default", "timestamp"]},
         {"event_name":"journey_enter", "params":["default", "timestamp"]},
         {"event_name":"journey_exit", "params":["default", "timestamp"]},
         {"event_name":"journey_product_action", "params":["default", "timestamp"]},
         {"event_name":"lead_collection_form_submit", "params":["default", "timestamp"]},
         {"event_name":"listing_page_view", "params":["default", "timestamp"]},
         {"event_name":"login", "params":["default", "timestamp"]},
         {"event_name":"logout", "params":["default", "timestamp"]},
         {"event_name":"mobile_recommendation_log", "params":["custom", "timestamp"]},
         {"event_name":"product_page_view", "params":["default", "timestamp"]},
         {"event_name":"app_push_delivered", "params":["default", "timestamp"]},
         {"event_name":"app_push_open", "params":["default", "timestamp"]},
         {"event_name":"recuperacao_de_email", "params":["custom", "timestamp"]},
         {"event_name":"recuperacao_de_senha", "params":["custom", "timestamp"]},
         {"event_name":"recuperar_conta", "params":["custom", "timestamp"]},
         {"event_name":"recuperar_email_login", "params":["custom", "timestamp"]},
         {"event_name":"retrospectiva_results", "params":["custom", "timestamp"]},
         {"event_name":"screen_journey", "params":["custom", "timestamp"]},
         {"event_name":"search", "params":["custom", "timestamp"]},
         {"event_name":"select_content", "params":["custom", "timestamp"]},
         {"event_name":"select_item", "params":["custom", "timestamp"]},
         {"event_name":"select_time", "params":["custom", "timestamp"]},
         {"event_name":"mobile_app_open", "params":["default", "timestamp"]},
         {"event_name":"inapp_view_from_app_push", "params":["default", "timestamp"]},
         {"event_name":"share", "params":["custom", "timestamp"]},
         {"event_name":"inapp_test_view", "params":["default", "timestamp"]},
         {"event_name":"verificar_beneficio", "params":["custom", "timestamp"]},
         {"event_name":"view_item", "params":["custom", "timestamp"]},
         {"event_name":"whatsapp_click", "params":["default", "timestamp"]},
         {"event_name":"whatsapp_delivered", "params":["default", "timestamp"]},
         {"event_name":"whatsapp_dropped", "params":["custom", "timestamp"]},
         {"event_name":"whatsapp_read", "params":["custom", "timestamp"]},
         {"event_name":"whatsapp_reply", "params":["default", "timestamp"]},
         {"event_name":"whatsapp_reply_first_button", "params":["default", "timestamp"]},
         {"event_name":"whatsapp_reply_other_reply", "params":["default", "timestamp"]},
         {"event_name":"whatsapp_undelivered", "params":["custom", "timestamp"]}
      ]
   },
   "format":"parquet",
   "hook":"https://insider-webhook-711516291484.us-central1.run.app/webhook_stream"
}'
