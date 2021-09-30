import datetime
import cloudscraper
import colorama
from termcolor import colored
import time
import json
import random
import pickle
from cryptography import fernet
import os
import bs4
import sys
import shutil
import requests, uuid, hashlib, hmac, urllib, string
from pathlib import Path
# Turn off InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# The urllib library was split into other modules from Python 2 to Python 3
if sys.version_info.major == 3:
    import urllib.parse

colorama.init()
key = b'HzodHGhHL2l4MjeYNm1k_FJa1QUemTKimQIKLpTtStY='

class P_InstaAPI:
    def __init__(self, creds):
        self.username = creds['username']
        self.password = creds['password']

        sessionpath = Path(f"sessions/{self.username}.session")

        mainlogin = P_InstagramLogin(self.username, self.password, Path("./sessions"))
        api = mainlogin.api

        if not api.isLoggedIn:
            print(colored(f"[{time.ctime()}] API: login failed", "red"))
            os.remove("secrets.pickle")
            shutil.rmtree("sessions/")
            exit()

        self.api = api

class P_InstagramAPI:
    API_URL = 'https://i.instagram.com/api/v1/'
    DEVICE_SETTINGS = {'manufacturer': 'Xiaomi',
                       'model': 'HM 1SW',
                       'android_version': 19,
                       'android_release': '6.4'}
    USER_AGENT = 'Instagram 89.0.0.21.101 Android ({android_version}/{android_release}; 320dpi; 720x1280; {manufacturer}; {model}; armani; qcom; fr_FR)'.format(**DEVICE_SETTINGS)
    IG_SIG_KEY = '4f8732eb9ba7d1c8e8897a75d6474d4eb3f5279137431b2aafb71fafe2abe178'
    EXPERIMENTS = 'ig_promote_reach_objective_fix_universe,ig_android_universe_video_production,ig_search_client_h1_2017_holdout,ig_android_live_follow_from_comments_universe,ig_android_carousel_non_square_creation,ig_android_live_analytics,ig_android_follow_all_dialog_confirmation_copy,ig_android_stories_server_coverframe,ig_android_video_captions_universe,ig_android_offline_location_feed,ig_android_direct_inbox_retry_seen_state,ig_android_ontact_invite_universe,ig_android_live_broadcast_blacklist,ig_android_insta_video_reconnect_viewers,ig_android_ad_async_ads_universe,ig_android_search_clear_layout_universe,ig_android_shopping_reporting,ig_android_stories_surface_universe,ig_android_verified_comments_universe,ig_android_preload_media_ahead_in_current_reel,android_instagram_prefetch_suggestions_universe,ig_android_reel_viewer_fetch_missing_reels_universe,ig_android_direct_search_share_sheet_universe,ig_android_business_promote_tooltip,ig_android_direct_blue_tab,ig_android_async_network_tweak_universe,ig_android_elevate_main_thread_priority_universe,ig_android_stories_gallery_nux,ig_android_instavideo_remove_nux_comments,ig_video_copyright_whitelist,ig_react_native_inline_insights_with_relay,ig_android_direct_thread_message_animation,ig_android_draw_rainbow_client_universe,ig_android_direct_link_style,ig_android_live_heart_enhancements_universe,ig_android_rtc_reshare,ig_android_preload_item_count_in_reel_viewer_buffer,ig_android_users_bootstrap_service,ig_android_auto_retry_post_mode,ig_android_shopping,ig_android_main_feed_seen_state_dont_send_info_on_tail_load,ig_fbns_preload_default,ig_android_gesture_dismiss_reel_viewer,ig_android_tool_tip,ig_android_ad_logger_funnel_logging_universe,ig_android_gallery_grid_column_count_universe,ig_android_business_new_ads_payment_universe,ig_android_direct_links,ig_android_audience_control,ig_android_live_encore_consumption_settings_universe,ig_perf_android_holdout,ig_android_cache_contact_import_list,ig_android_links_receivers,ig_android_ad_impression_backtest,ig_android_list_redesign,ig_android_stories_separate_overlay_creation,ig_android_stop_video_recording_fix_universe,ig_android_render_video_segmentation,ig_android_live_encore_reel_chaining_universe,ig_android_sync_on_background_enhanced_10_25,ig_android_immersive_viewer,ig_android_mqtt_skywalker,ig_fbns_push,ig_android_ad_watchmore_overlay_universe,ig_android_react_native_universe,ig_android_profile_tabs_redesign_universe,ig_android_live_consumption_abr,ig_android_story_viewer_social_context,ig_android_hide_post_in_feed,ig_android_video_loopcount_int,ig_android_enable_main_feed_reel_tray_preloading,ig_android_camera_upsell_dialog,ig_android_ad_watchbrowse_universe,ig_android_internal_research_settings,ig_android_search_people_tag_universe,ig_android_react_native_ota,ig_android_enable_concurrent_request,ig_android_react_native_stories_grid_view,ig_android_business_stories_inline_insights,ig_android_log_mediacodec_info,ig_android_direct_expiring_media_loading_errors,ig_video_use_sve_universe,ig_android_cold_start_feed_request,ig_android_enable_zero_rating,ig_android_reverse_audio,ig_android_branded_content_three_line_ui_universe,ig_android_live_encore_production_universe,ig_stories_music_sticker,ig_android_stories_teach_gallery_location,ig_android_http_stack_experiment_2017,ig_android_stories_device_tilt,ig_android_pending_request_search_bar,ig_android_fb_topsearch_sgp_fork_request,ig_android_seen_state_with_view_info,ig_android_animation_perf_reporter_timeout,ig_android_new_block_flow,ig_android_story_tray_title_play_all_v2,ig_android_direct_address_links,ig_android_stories_archive_universe,ig_android_save_collections_cover_photo,ig_android_live_webrtc_livewith_production,ig_android_sign_video_url,ig_android_stories_video_prefetch_kb,ig_android_stories_create_flow_favorites_tooltip,ig_android_live_stop_broadcast_on_404,ig_android_live_viewer_invite_universe,ig_android_promotion_feedback_channel,ig_android_render_iframe_interval,ig_android_accessibility_logging_universe,ig_android_camera_shortcut_universe,ig_android_use_one_cookie_store_per_user_override,ig_profile_holdout_2017_universe,ig_android_stories_server_brushes,ig_android_ad_media_url_logging_universe,ig_android_shopping_tag_nux_text_universe,ig_android_comments_single_reply_universe,ig_android_stories_video_loading_spinner_improvements,ig_android_collections_cache,ig_android_comment_api_spam_universe,ig_android_facebook_twitter_profile_photos,ig_android_shopping_tag_creation_universe,ig_story_camera_reverse_video_experiment,ig_android_direct_bump_selected_recipients,ig_android_ad_cta_haptic_feedback_universe,ig_android_vertical_share_sheet_experiment,ig_android_family_bridge_share,ig_android_search,ig_android_insta_video_consumption_titles,ig_android_stories_gallery_preview_button,ig_android_fb_auth_education,ig_android_camera_universe,ig_android_me_only_universe,ig_android_instavideo_audio_only_mode,ig_android_user_profile_chaining_icon,ig_android_live_video_reactions_consumption_universe,ig_android_stories_hashtag_text,ig_android_post_live_badge_universe,ig_android_swipe_fragment_container,ig_android_search_users_universe,ig_android_live_save_to_camera_roll_universe,ig_creation_growth_holdout,ig_android_sticker_region_tracking,ig_android_unified_inbox,ig_android_live_new_watch_time,ig_android_offline_main_feed_10_11,ig_import_biz_contact_to_page,ig_android_live_encore_consumption_universe,ig_android_experimental_filters,ig_android_search_client_matching_2,ig_android_react_native_inline_insights_v2,ig_android_business_conversion_value_prop_v2,ig_android_redirect_to_low_latency_universe,ig_android_ad_show_new_awr_universe,ig_family_bridges_holdout_universe,ig_android_background_explore_fetch,ig_android_following_follower_social_context,ig_android_video_keep_screen_on,ig_android_ad_leadgen_relay_modern,ig_android_profile_photo_as_media,ig_android_insta_video_consumption_infra,ig_android_ad_watchlead_universe,ig_android_direct_prefetch_direct_story_json,ig_android_shopping_react_native,ig_android_top_live_profile_pics_universe,ig_android_direct_phone_number_links,ig_android_stories_weblink_creation,ig_android_direct_search_new_thread_universe,ig_android_histogram_reporter,ig_android_direct_on_profile_universe,ig_android_network_cancellation,ig_android_background_reel_fetch,ig_android_react_native_insights,ig_android_insta_video_audio_encoder,ig_android_family_bridge_bookmarks,ig_android_data_usage_network_layer,ig_android_universal_instagram_deep_links,ig_android_dash_for_vod_universe,ig_android_modular_tab_discover_people_redesign,ig_android_mas_sticker_upsell_dialog_universe,ig_android_ad_add_per_event_counter_to_logging_event,ig_android_sticky_header_top_chrome_optimization,ig_android_rtl,ig_android_biz_conversion_page_pre_select,ig_android_promote_from_profile_button,ig_android_live_broadcaster_invite_universe,ig_android_share_spinner,ig_android_text_action,ig_android_own_reel_title_universe,ig_promotions_unit_in_insights_landing_page,ig_android_business_settings_header_univ,ig_android_save_longpress_tooltip,ig_android_constrain_image_size_universe,ig_android_business_new_graphql_endpoint_universe,ig_ranking_following,ig_android_stories_profile_camera_entry_point,ig_android_universe_reel_video_production,ig_android_power_metrics,ig_android_sfplt,ig_android_offline_hashtag_feed,ig_android_live_skin_smooth,ig_android_direct_inbox_search,ig_android_stories_posting_offline_ui,ig_android_sidecar_video_upload_universe,ig_android_promotion_manager_entry_point_universe,ig_android_direct_reply_audience_upgrade,ig_android_swipe_navigation_x_angle_universe,ig_android_offline_mode_holdout,ig_android_live_send_user_location,ig_android_direct_fetch_before_push_notif,ig_android_non_square_first,ig_android_insta_video_drawing,ig_android_swipeablefilters_universe,ig_android_live_notification_control_universe,ig_android_analytics_logger_running_background_universe,ig_android_save_all,ig_android_reel_viewer_data_buffer_size,ig_direct_quality_holdout_universe,ig_android_family_bridge_discover,ig_android_react_native_restart_after_error_universe,ig_android_startup_manager,ig_story_tray_peek_content_universe,ig_android_profile,ig_android_high_res_upload_2,ig_android_http_service_same_thread,ig_android_scroll_to_dismiss_keyboard,ig_android_remove_followers_universe,ig_android_skip_video_render,ig_android_story_timestamps,ig_android_live_viewer_comment_prompt_universe,ig_profile_holdout_universe,ig_android_react_native_insights_grid_view,ig_stories_selfie_sticker,ig_android_stories_reply_composer_redesign,ig_android_streamline_page_creation,ig_explore_netego,ig_android_ig4b_connect_fb_button_universe,ig_android_feed_util_rect_optimization,ig_android_rendering_controls,ig_android_os_version_blocking,ig_android_encoder_width_safe_multiple_16,ig_search_new_bootstrap_holdout_universe,ig_android_snippets_profile_nux,ig_android_e2e_optimization_universe,ig_android_comments_logging_universe,ig_shopping_insights,ig_android_save_collections,ig_android_live_see_fewer_videos_like_this_universe,ig_android_show_new_contact_import_dialog,ig_android_live_view_profile_from_comments_universe,ig_fbns_blocked,ig_formats_and_feedbacks_holdout_universe,ig_android_reduce_view_pager_buffer,ig_android_instavideo_periodic_notif,ig_search_user_auto_complete_cache_sync_ttl,ig_android_marauder_update_frequency,ig_android_suggest_password_reset_on_oneclick_login,ig_android_promotion_entry_from_ads_manager_universe,ig_android_live_special_codec_size_list,ig_android_enable_share_to_messenger,ig_android_background_main_feed_fetch,ig_android_live_video_reactions_creation_universe,ig_android_channels_home,ig_android_sidecar_gallery_universe,ig_android_upload_reliability_universe,ig_migrate_mediav2_universe,ig_android_insta_video_broadcaster_infra_perf,ig_android_business_conversion_social_context,android_ig_fbns_kill_switch,ig_android_live_webrtc_livewith_consumption,ig_android_destroy_swipe_fragment,ig_android_react_native_universe_kill_switch,ig_android_stories_book_universe,ig_android_all_videoplayback_persisting_sound,ig_android_draw_eraser_universe,ig_direct_search_new_bootstrap_holdout_universe,ig_android_cache_layer_bytes_threshold,ig_android_search_hash_tag_and_username_universe,ig_android_business_promotion,ig_android_direct_search_recipients_controller_universe,ig_android_ad_show_full_name_universe,ig_android_anrwatchdog,ig_android_qp_kill_switch,ig_android_2fac,ig_direct_bypass_group_size_limit_universe,ig_android_promote_simplified_flow,ig_android_share_to_whatsapp,ig_android_hide_bottom_nav_bar_on_discover_people,ig_fbns_dump_ids,ig_android_hands_free_before_reverse,ig_android_skywalker_live_event_start_end,ig_android_live_join_comment_ui_change,ig_android_direct_search_story_recipients_universe,ig_android_direct_full_size_gallery_upload,ig_android_ad_browser_gesture_control,ig_channel_server_experiments,ig_android_video_cover_frame_from_original_as_fallback,ig_android_ad_watchinstall_universe,ig_android_ad_viewability_logging_universe,ig_android_new_optic,ig_android_direct_visual_replies,ig_android_stories_search_reel_mentions_universe,ig_android_threaded_comments_universe,ig_android_mark_reel_seen_on_Swipe_forward,ig_internal_ui_for_lazy_loaded_modules_experiment,ig_fbns_shared,ig_android_capture_slowmo_mode,ig_android_live_viewers_list_search_bar,ig_android_video_single_surface,ig_android_offline_reel_feed,ig_android_video_download_logging,ig_android_last_edits,ig_android_exoplayer_4142,ig_android_post_live_viewer_count_privacy_universe,ig_android_activity_feed_click_state,ig_android_snippets_haptic_feedback,ig_android_gl_drawing_marks_after_undo_backing,ig_android_mark_seen_state_on_viewed_impression,ig_android_live_backgrounded_reminder_universe,ig_android_live_hide_viewer_nux_universe,ig_android_live_monotonic_pts,ig_android_search_top_search_surface_universe,ig_android_user_detail_endpoint,ig_android_location_media_count_exp_ig,ig_android_comment_tweaks_universe,ig_android_ad_watchmore_entry_point_universe,ig_android_top_live_notification_universe,ig_android_add_to_last_post,ig_save_insights,ig_android_live_enhanced_end_screen_universe,ig_android_ad_add_counter_to_logging_event,ig_android_blue_token_conversion_universe,ig_android_exoplayer_settings,ig_android_progressive_jpeg,ig_android_offline_story_stickers,ig_android_gqls_typing_indicator,ig_android_chaining_button_tooltip,ig_android_video_prefetch_for_connectivity_type,ig_android_use_exo_cache_for_progressive,ig_android_samsung_app_badging,ig_android_ad_holdout_watchandmore_universe,ig_android_offline_commenting,ig_direct_stories_recipient_picker_button,ig_insights_feedback_channel_universe,ig_android_insta_video_abr_resize,ig_android_insta_video_sound_always_on'
    SIG_KEY_VERSION = '4'

    def __init__(self, username, password):
        m = hashlib.md5()
        m.update(username.encode('utf-8') + password.encode('utf-8'))
        self.device_id = self.generateDeviceId(m.hexdigest())
        self.isLoggedIn = False
        self.LastResponse = None
        self.PATH = ""
        self.s = requests.Session()

        self.username = username
        self.password = password
        self.uuid = self.generateUUID(True)

    def sendMessage(self, target_user, msgText):
        target_user = f'[[{",".join([target_user])}]]'

        url = 'direct_v2/threads/broadcast/text/'

        data = {
            'text': msgText,
            '_uuid': self.uuid,
            '_csrftoken': self.token,
            'recipient_users': target_user,
            '_uid': self.username_id,
            'action': 'send_item',
            'client_context': self.generateUUID(True)
        }

        return self.SendRequest(url, data)

    def login(self, force=False):
        if (not self.isLoggedIn or force):
            if (self.SendRequest('si/fetch_headers/?challenge_type=signup&guid=' + self.generateUUID(False), None, True)):
                data = {'phone_id': self.generateUUID(True),
                        '_csrftoken': self.LastCookies['csrftoken'],
                        'username': self.username,
                        'guid': self.uuid,
                        'device_id': self.device_id,
                        'password': self.password,
                        'login_attempt_count': '0'}

                if (self.SendRequest('accounts/login/', self.generateSignature(json.dumps(data)), True)):
                    self.isLoggedIn = True
                    self.username_id = self.logged_in_user_pk
                    self.rank_token = f"{self.username_id}_{self.uuid}"
                    self.token = self.LastCookies["csrftoken"]
                    self.syncFeatures()
                    self.autoCompleteUserList()
                    self.timelineFeed()
                    self.getv2Inbox()
                    self.getRecentActivity()
                    return True

    def syncFeatures(self):
        data = json.dumps({'_uuid': self.uuid,
                           '_uid': self.username_id,
                           'id': self.username_id,
                           '_csrftoken': self.token,
                           'experiments': self.EXPERIMENTS})
        return self.SendRequest('qe/sync/', self.generateSignature(data))

    def autoCompleteUserList(self):
        return self.SendRequest('friendships/autocomplete_user_list/')

    def getRecentActivity(self):
        activity = self.SendRequest('news/inbox/?')
        return activity

    def timelineFeed(self):
        return self.SendRequest('feed/timeline/')

    def getv2Inbox(self, limit=50):
        inbox = self.SendRequest(
            'direct_v2/inbox/?persistentBadging=true&use_unified_inbox=true&limit={}'.format(limit))
        return inbox

    def generateSignature(self, data, skip_quote=False):
        if not skip_quote:
            try:
                parsedData = urllib.parse.quote(data)
            except AttributeError:
                parsedData = urllib.quote(data)
        else:
            parsedData = data
        return 'ig_sig_key_version=' + self.SIG_KEY_VERSION + '&signed_body=' + hmac.new(
            self.IG_SIG_KEY.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest() + '.' + parsedData

    def generateDeviceId(self, seed):
        volatile_seed = "12345"
        m = hashlib.md5()
        m.update(seed.encode('utf-8') + volatile_seed.encode('utf-8'))
        return 'android-' + m.hexdigest()[:16]

    def generateUUID(self, type):
        generated_uuid = str(uuid.uuid4())
        if (type):
            return generated_uuid
        else:
            return generated_uuid.replace('-', '')

    def SendRequest(self, endpoint, post=None, login=False, wait=20):
        verify = False  # Don't show request warning

        if (not self.isLoggedIn and not login):
            raise Exception("Not logged in!\n")

        self.s.headers.update(
            {'Connection': 'close',
             'Accept': '*/*',
             'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
             'Cookie2': '$Version=1',
             'Accept-Language': 'en-US',
             'User-Agent': self.USER_AGENT})

        while True:
            try:
                if (post is not None):
                    response = self.s.post(self.API_URL + endpoint, data=post, verify=verify)
                else:
                    response = self.s.get(self.API_URL + endpoint, verify=verify)
                break
            except Exception as e:
                print('Except on SendRequest (wait 60 sec and resend): ' + str(e))
                time.sleep(60)

        if response.status_code == 200:
            self.LastCookies = response.cookies
            try: self.logged_in_user_pk = json.loads(response.text)['logged_in_user']['pk']
            except: pass
            return response.status_code, json.loads(response.text)
        else:
            if response.status_code != 405:
                print(colored(f"[{time.ctime()}] API: login failed", "red"))
                os.remove("secrets.pickle")
                shutil.rmtree("sessions/")
                exit()

            try:
                self.LastCookies = response.cookies
                try: self.logged_in_user_pk = json.loads(response.text)['logged_in_user']['pk']
                except: pass
                return response.status_code, json.loads(response.text)
            except:
                pass

            return False

    def default_data(self):
        return {"_uuid": self.uuid, "_uid": self.username_id, "_csrftoken": self.token}


class P_InstagramLogin(object):
    def __init__(self, username, password, folder=Path("./")):
        encrypt_creds = fernet.Fernet(key)
        self.username = username
        self.password = password
        self.path = Path(str(folder) + "/" + username + ".session")

        if not os.path.exists(str(folder)):
            os.mkdir(folder)

        if not os.path.exists(self.path):
            self.api = P_InstagramAPI(self.username, self.password)
            try:
                self.api.login()
            except KeyError:  # logged_in_user -> couldn't login 
                shutil.rmtree("sessions/")
                exit()

            self.api.password = encrypt_creds.encrypt(str.encode(self.password))
            pickle.dump(self.api, open(self.path, "wb"))
            self.api.password = encrypt_creds.decrypt(self.api.password)
        else:
            self.api = pickle.load(open(self.path, "rb"))
            self.api.password = encrypt_creds.decrypt(self.api.password)

            if not self.api.isLoggedIn:
                self.api.login()
                if self.api.isLoggedIn:
                    pickle.dump(self.api, open(self.path, "wb"))


class Scraper:
    def __init__(self, accept):
        self.banner()

        self.scraper = cloudscraper.create_scraper()

        self.link = 'https://www.instagram.com/accounts/login/'
        self.login_url = 'https://www.instagram.com/accounts/login/ajax/'

        self.time = int(datetime.datetime.now().timestamp())

        response = self.scraper.get(self.link)
        try:
            self.csrf = response.cookies['csrftoken']
        except:
            self.csrf = "bguzeiugege"
        self.acceptRequests = accept

        if os.path.exists("accept.json"):
            self.acceptRequests=False

        self.csrf_token = None

        self.username = None
        self.password = None

        self.new_requests = 0
        self.pending_users = {}

        self.accepted = []

        self.totalProgress = []

        self.save_login_credentials()

        self.payload = {
            'username': self.username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{self.time}:{self.password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        self.login_header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/49.0.2623.112 Safari/537.36',

            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/accounts/login/",
            "x-csrftoken": self.csrf
        }

        # Maintaining the acquired login session

        self.scraper = cloudscraper.CloudScraper()

        self.login()
        self.run()

        self.remove = "0"

        self.p_ = ["0"]
        self.period = 50
        for e in range(self.period):
            self.p_.append(".")

        self.start = time.perf_counter()

    def progress(self, user, e, total):
        total_max = total
        total = total_max - 1

        try:
            p = "".join(self.p_)
            percentage = round(e / total * 100, 2)

            now = time.perf_counter() - self.start

            num = str(now).split("e")[0]
            perc = float(num)

            if int(percentage) > 0:
                time_remaining = 100 * perc / round(percentage)

                sys.stdout.write("\r" + colored(round(time_remaining - now, 5), 'magenta')
                                 + "|t/s| processing users: " + user + " " + "[" + colored(p.split(self.remove)[0],
                                                                                           "magenta") + colored(
                    str(percentage) + "%",
                    "yellow") +
                                 p.split(self.remove)[1] + " ]" + "time remaining: " + str(
                    datetime.datetime.now() + datetime.timedelta(
                        seconds=round(time_remaining - now)) - datetime.datetime.now()))
                sys.stdout.flush()
                time.sleep(0.3)
            iter_index = round(e / total * self.period)

            current_position = self.p_.index(self.remove)
            self.p_.pop(current_position)
            if e == total - 2 or e == total or e == total - 1:
                self.p_.append(str(percentage) + "%")
            else:
                self.p_.insert(iter_index, str(percentage) + "%")
            self.remove = str(percentage) + "%"
        except:
            percentage = "0"

    def save_login_credentials(self):
        encrypt_creds = fernet.Fernet(key)
        if os.path.exists("secrets.pickle"):

            with open("secrets.pickle", "rb") as f:
                decrypt_pickle = pickle.load(f)
                decrypt_cryptography = encrypt_creds.decrypt(decrypt_pickle)
                decrypt_pickle2 = pickle.loads(decrypt_cryptography)
                self.username = decrypt_pickle2.get("username", "specify a username")
                self.password = decrypt_pickle2.get("password", "specify a password")

                self.p_api = P_InstaAPI({"username": self.username, "password": self.password})
        else:
            print(colored("[+] Creating credentials file", "green"))
            self.username = input("Enter username: ")
            self.password = input("Enter password: ")
            credentials = {"username": self.username, "password": self.password}

            pickled_credentials = pickle.dumps(credentials)
            encrypted = encrypt_creds.encrypt(pickled_credentials)
            with open("secrets.pickle", "wb") as f:
                pickle.dump(encrypted, f)

            self.p_api = P_InstaAPI(credentials)

    def login(self):
        # Logging the user in
        login_response = self.scraper.post(self.login_url, data=self.payload, headers=self.login_header)
        json_data = json.loads(login_response.text)
        if json_data.get("authenticated"):
            print(colored("\n[+] Successfully logged in", "green"))
            cookies = login_response.cookies
            cookie_jar = cookies.get_dict()
            self.csrf_token = cookie_jar['csrftoken']
            print("csrf_token:", self.csrf_token)
            session_id = cookie_jar['sessionid']
            user_id = cookie_jar['ds_user_id']
            print("session_id:", session_id)
        else:
            print(colored(f"[{time.ctime()}] cloudscraper: login failed {login_response.text}", "red"))
            os.remove("secrets.pickle")
            shutil.rmtree("sessions/")
            exit()

        try:
            time.sleep(random.randrange(2, 5))
            user = self.scraper.get(f"https://www.instagram.com/{self.username}/")
            logged_user = str(bs4.BeautifulSoup(user.text, 'lxml').title.text).split('•')[0]
            if "is on Instagram " in logged_user:
                print(colored(f"\n[+] {time.ctime()} logged in as {logged_user.replace('is on Instagram', '')}", "blue"))
            else:
                try:
                    print(colored(f"\n[+] {time.ctime()} logged in as {logged_user.replace('is on Instagram', '')}", "blue"))
                except:
                    print(colored(f"\n[+] {time.ctime()} logged in as {logged_user}", "blue"))

        except Exception:
            print(colored(f"\n[+] logged in as {self.username}", "blue"))

        self.user_id = json_data['userId']
        self.uuid = self.generateUUID(True)

    def pending_requests(self):
        # Get the pending users

        parameter = {"variables": {"fetch_media_count": 0, "fetch_suggested_count": 30, "ignore_cache": True,
                                   "filter_followed_friends": True, "seen_ids": [], "include_reel": True}}
        t = json.dumps(parameter)
        time.sleep(random.randrange(1, 4))

        headers = {
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, '
                          'like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; '
                          'scale=2.00; 828x1792; 165586599) '
        }

        r = self.scraper.get("https://i.instagram.com/api/v1/friendships/pending/", headers=headers)
        print(f"\n{('═'*48)}\n\n[+] Pending follow requests")

        pending = []
        pending_total = 0
        for e, data in enumerate(r.json()['users']):
            e += 1
            print(f"[{e}] {data['username']}")
            pending.append(data["username"])
            pending_total += 1
            self.totalProgress.append(data)

        if self.acceptRequests:
            # Accept the obtained requests
            user_num = 1
            for user in pending:
                self.accept_request(user, user_num)
                self.accepted.append(user)
                pending_total -= 1
                user_num += 1
            try:
                for pending_user in self.accepted:
                    pending.remove(pending_user)
            except:
                pending.clear()

        self.pending_users.update({f"username": pending, "total_requests": [pending_total]})

    def process_users(self):
        if os.path.exists(f"{self.username}_pending_users.json"):
            total_pending = 0
            newRequest = 0
            processed_users = []
            f = open(f"{self.username}_pending_users.json", "r")
            data = json.load(f)

            for e, user in enumerate(self.pending_users["username"]):
                self.progress(user, e, len(self.pending_users['username']))

                if user in data["username"] or user in self.accepted:
                    pass
                else:
                    newRequest += 1
                    print(colored(f"[+] New request from {user}", "green"))
                    processed_users.append(user)
                    if user in data["username"]:
                        processed_users.remove(user)
            if len(self.pending_users["username"]) >= 200:
                # If pending requests are more than 200 add to previous data count
                total_pending += data["total_requests"][0] + newRequest
            else:
                total_pending += self.pending_users["total_requests"][0]

            # Use this to get the rate of users

            self.new_requests = newRequest
            print(f"\n{self.username} has {total_pending} pending follow requests")
            f.close()
            f2 = open(f"{self.username}_pending_users.json", "w")
            if self.acceptRequests:

                json.dump({"username": self.pending_users['username'], "total_requests": [total_pending],
                           "accepted": self.accepted}, f2, indent=4, sort_keys=True)
                f2.close()
            else:
                json.dump({"username": data["username"] + processed_users, "total_requests": [total_pending],
                           "accepted": self.accepted}, f2, indent=4, sort_keys=True)
                f2.close()

        else:
            with open(f"{self.username}_pending_users.json", "w") as f:
                json.dump(self.pending_users, f, indent=4, sort_keys=True)
            print(f"\n{self.username} has {self.pending_users['total_requests'][0]} pending follow requests")
            total_pending = self.pending_users["total_requests"][0]

        self.send_msg(total_pending)

    def get_user_id(self, username):
        # Get the users info
        id = self.scraper.get(f"https://www.instagram.com/{username}/?__a=1")
        id_data = id.json()
        user_data = id_data["graphql"]["user"]
        full_name = user_data.get("username")
        user_id = user_data.get("id")
        return {"id": user_id, "username": full_name}

    def accept_request(self, accept_user, current_user):
        # Accept the parsed user
        headers = {
            'content-length': '0',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, '
                          'like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; '
                          'scale=2.00; 828x1792; 165586599) ',
            "x-csrftoken": self.csrf_token
        }
        requested_user = self.get_user_id(accept_user)
        id = requested_user.get("id")
        username = requested_user.get("username")
        accept = self.scraper.post(f"https://www.instagram.com/web/friendships/{id}/approve/", headers=headers)
        sys.stdout.write(colored(
            f"\r[+] {round(current_user / len(self.totalProgress) * 100, 2)}% accepted",
            "green"))
        sys.stdout.flush()
        time.sleep(0.1)

    def accept_all(self):
        if not os.path.exists("accept.json") and self.acceptRequests:
            sys.stdout.write("\r[+] Accepting follow requests")
            sys.stdout.flush()
            time.sleep(1)

            while True:
                # if len(self.pending_users['username']) == 0:
                if len(self.pending_users['username']) < 200:
                    sys.stdout.write("\r[+] Reached the maximum amount to accept for this run, will check again in next run")
                    sys.stdout.flush()
                    time.sleep(1)
                    break
                else:
                    self.pending_requests()
                    self.process_users()
                    time.sleep(random.randrange(3, 7))
                
            sys.stdout.write(f"\r[+] No more follow requests to accept, all incoming requests will not be accepted anymore")
            sys.stdout.flush()

            f = open("accept.json", "w")
            json.dump({'accept': False}, f)
            f.close()

            print("\n")
            self.acceptRequests = False
        else:
            pass
            # Still needs to accept

    def generateUUID(self, type_):
        generated_uuid = str(uuid.uuid4())
        if (type_):
            return generated_uuid
        else:
            return generated_uuid.replace('-', '')

    def send_msg(self, total_pending):
        try:
            if self.acceptRequests == False:
                self.p_api.api.sendMessage(
                    self.user_id,
                    f"Pending follow requests: {total_pending}\n\n"
                    f"Date: {time.ctime()}\n\n"
                    f"User: @{self.username}\n"
                    f"User ID: {self.user_id}"
                )
            else:
                self.p_api.api.sendMessage(
                    self.user_id,
                    "Accepting follow requests\n\n"
                    f"Date: {time.ctime()}\n\n"
                    f"User: @{self.username}\n"
                    f"User ID: {self.user_id}"
                )
        except Exception as e:
            print("Unable to send DM ->", e)
            print(self.p_api.api.LastResponse)

    def run(self):
        self.waiting = random.randint(3600, 4200)

        def runScraper():
            while True:
                if self.new_requests >= 50:
                    self.waiting = random.randint(2400, 3000)
                    
                if self.new_requests >= 100:
                    self.waiting = random.randint(1800, 2400)

                if self.new_requests >= 150:
                    self.waiting = random.randint(900, 1200)
                
                self.pending_requests()
                self.process_users()
                self.remove = "0"

                self.p_ = ["0"]
                self.period = 50
                for e in range(self.period):
                    self.p_.append(".")

                self.accept_all()
                
                print(colored(f"[{time.ctime()}] Next run in {round((self.waiting/60))} minutes", "blue"))
                time.sleep(self.waiting)

        runScraper()

    def banner(self):
        print(colored('''
██████╗ ███████╗ ██████╗ ██╗   ██╗███████╗███████╗████████╗    ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ 
██╔══██╗██╔════╝██╔═══██╗██║   ██║██╔════╝██╔════╝╚══██╔══╝    ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗
██████╔╝█████╗  ██║   ██║██║   ██║█████╗  ███████╗   ██║       ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
██╔══██╗██╔══╝  ██║▄▄ ██║██║   ██║██╔══╝  ╚════██║   ██║       ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
██║  ██║███████╗╚██████╔╝╚██████╔╝███████╗███████║   ██║       ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║
╚═╝  ╚═╝╚══════╝ ╚══▀▀═╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝       ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
        ''', "blue"), end="\n")

if __name__ == "__main__":
    '''
    To accept follow requests -> Scraper(accept=True)
    
    Will accept every run until your follow requests are below 200
    Can only accept a maximum amount of 200 requested users per run
    '''
    Scraper(accept=False)
